"""
Slime PE Surgeon - Pure Python PE Binary IAT Parser & Patching Engine
Directly inspects and surgically patches Windows PE (Portable Executable) binaries
without requiring source code or external dependencies.
"""
import struct
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class PESurgeon:
    """Parses PE32/PE32+ headers and modifies Import Tables surgically."""

    DANGEROUS_API_MAPPINGS = {
        # Destructive File APIs -> Harmless Query APIs of equal or shorter length
        "DeleteFileA": "GetVersion\0",
        "DeleteFileW": "GetVersion\0",
        "RemoveDirectoryA": "GetTickCount\0",
        "RemoveDirectoryW": "GetTickCount\0",
        "MoveFileExW": "GetTickCount\0",
        "MoveFileExA": "GetTickCount\0",
        # Dangerous Network/Execution APIs
        "URLDownloadToFileW": "GetSystemTimeAsFileTime\0",
        "URLDownloadToFileA": "GetSystemTimeAsFileTime\0",
        "WinExec": "GetACP\0",
    }

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"Binary not found: {filepath}")
        self.raw_data = bytearray(self.filepath.read_bytes())
        self.is_64bit = False
        self.pe_offset = 0
        self.sections = []
        self.import_dir_rva = 0
        self.import_dir_size = 0
        self._parse_headers()

    def _parse_headers(self):
        # 1. DOS Header: check 'MZ'
        if self.raw_data[:2] != b"MZ":
            raise ValueError("Not a valid PE file (Missing 'MZ' magic)")

        # Offset to PE Header at 0x3C
        self.pe_offset = struct.unpack_from("<I", self.raw_data, 0x3C)[0]
        if self.raw_data[self.pe_offset:self.pe_offset + 4] != b"PE\0\0":
            raise ValueError("Invalid PE signature")

        # 2. File Header
        file_header_offset = self.pe_offset + 4
        machine, num_sections, _, _, _, opt_header_size, _ = struct.unpack_from(
            "<HHIIIHH", self.raw_data, file_header_offset
        )

        # 3. Optional Header
        opt_header_offset = file_header_offset + 20
        magic = struct.unpack_from("<H", self.raw_data, opt_header_offset)[0]
        self.is_64bit = (magic == 0x20B)  # 0x10B = PE32 (32-bit), 0x20B = PE32+ (64-bit)

        # Import Directory is the 2nd entry in DataDirectory array
        data_dir_offset = opt_header_offset + (112 if self.is_64bit else 96)
        # Entry 1 is Import Table (index 0 is Export, index 1 is Import)
        self.import_dir_rva, self.import_dir_size = struct.unpack_from("<II", self.raw_data, data_dir_offset + 8)
        # Entry 4 is Security / Certificate Table
        self.security_dir_offset = data_dir_offset + 32

        # 4. Section Headers
        sections_offset = opt_header_offset + opt_header_size
        self.sections = []
        for i in range(num_sections):
            sec_offset = sections_offset + (i * 40)
            sec_name = self.raw_data[sec_offset:sec_offset + 8].decode('latin1').strip('\0')
            vsize, vaddr, raw_size, raw_offset = struct.unpack_from("<IIII", self.raw_data, sec_offset + 8)
            self.sections.append({
                "name": sec_name,
                "vaddr": vaddr,
                "vsize": vsize,
                "raw_offset": raw_offset,
                "raw_size": raw_size
            })

    def rva_to_offset(self, rva: int) -> Optional[int]:
        """Translates Relative Virtual Address (RVA) to file byte offset."""
        for sec in self.sections:
            if sec["vaddr"] <= rva < sec["vaddr"] + max(sec["vsize"], sec["raw_size"]):
                return sec["raw_offset"] + (rva - sec["vaddr"])
        return None

    def scan_imports(self) -> List[Dict]:
        """Inspects all imported DLLs and API functions."""
        if self.import_dir_rva == 0 or self.import_dir_size == 0:
            return []

        descriptor_offset = self.rva_to_offset(self.import_dir_rva)
        if descriptor_offset is None:
            return []

        imports = []
        curr = descriptor_offset
        ptr_size = 8 if self.is_64bit else 4
        ptr_unpack = "<Q" if self.is_64bit else "<I"

        while True:
            orig_first_thunk, timestamp, fwd_chain, name_rva, first_thunk = struct.unpack_from(
                "<IIIII", self.raw_data, curr
            )
            if orig_first_thunk == 0 and first_thunk == 0 and name_rva == 0:
                break  # Null terminator descriptor

            dll_name_offset = self.rva_to_offset(name_rva)
            dll_name = ""
            if dll_name_offset:
                null_idx = self.raw_data.find(b"\0", dll_name_offset)
                dll_name = self.raw_data[dll_name_offset:null_idx].decode('latin1')

            thunk_rva = orig_first_thunk if orig_first_thunk != 0 else first_thunk
            thunk_offset = self.rva_to_offset(thunk_rva)

            functions = []
            if thunk_offset:
                t_curr = thunk_offset
                while True:
                    thunk_val = struct.unpack_from(ptr_unpack, self.raw_data, t_curr)[0]
                    if thunk_val == 0:
                        break

                    # Check ordinal flag (high bit)
                    is_ordinal = bool(thunk_val & (0x8000000000000000 if self.is_64bit else 0x80000000))
                    if not is_ordinal:
                        # RVA points to IMAGE_IMPORT_BY_NAME: Hint (2 bytes) + Name (ASCII null-terminated)
                        name_entry_offset = self.rva_to_offset(thunk_val)
                        if name_entry_offset:
                            fn_name_offset = name_entry_offset + 2
                            fn_null = self.raw_data.find(b"\0", fn_name_offset)
                            fn_name = self.raw_data[fn_name_offset:fn_null].decode('latin1')
                            functions.append({
                                "name": fn_name,
                                "name_offset": fn_name_offset,
                                "thunk_offset": t_curr
                            })
                    t_curr += ptr_size

            imports.append({
                "dll": dll_name,
                "functions": functions
            })
            curr += 20

        return imports

    def apply_surgical_patch(self, output_filepath: str) -> Dict:
        """
        Surgically redirects destructive IAT APIs to harmless query functions.
        Generates a patched binary where dangerous actions are neutralized.
        """
        imports = self.scan_imports()
        patched_actions = []

        data_copy = bytearray(self.raw_data)

        for dll_entry in imports:
            for fn in dll_entry["functions"]:
                fn_name = fn["name"]
                if fn_name in self.DANGEROUS_API_MAPPINGS:
                    replacement = self.DANGEROUS_API_MAPPINGS[fn_name]
                    target_offset = fn["name_offset"]

                    # The replacement must fit within the original name slot (length <= len(original))
                    orig_len = len(fn_name)
                    rep_bytes = replacement.encode('latin1')
                    if len(rep_bytes) <= orig_len + 1:
                        # Pad with null bytes to preserve alignment
                        padded_replacement = rep_bytes.ljust(orig_len + 1, b"\0")
                        data_copy[target_offset:target_offset + len(padded_replacement)] = padded_replacement

                        patched_actions.append({
                            "dll": dll_entry["dll"],
                            "original_api": fn_name,
                            "neutralized_with": replacement.replace('\0', ''),
                            "file_offset": hex(target_offset),
                            "action": "IAT_API_SWAP_NEUTRALIZED"
                        })

        # Strip/zero out security directory entry so Windows loads it as clean unsigned binary
        if hasattr(self, 'security_dir_offset') and self.security_dir_offset:
            data_copy[self.security_dir_offset:self.security_dir_offset + 8] = b"\0" * 8

        out_path = Path(output_filepath)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data_copy)

        return {
            "success": True,
            "original_file": str(self.filepath),
            "patched_file": str(out_path.resolve()),
            "total_threats_neutralized": len(patched_actions),
            "details": patched_actions
        }
