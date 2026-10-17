"""
Slime Binary Surgeon CLI - Direct IAT Parser & Patching Tool
Allows users to inspect and surgically patch any Windows PE binary (.exe / .dll).
"""
import sys
import os
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.pe_surgeon import PESurgeon

BANNER = r"""
   ╔═══════════════════════════════════════════════════════════════╗
   ║      🟢 史萊姆二進制外科手術引擎 (SLIME PE SURGEON)           ║
   ║    不需要原始碼 • 零編譯 • 直接對 Windows PE / .exe 進行 IAT 熱補丁    ║
   ╚═══════════════════════════════════════════════════════════════╝
"""

def inspect_binary(filepath: str):
    print(BANNER)
    print(f"🔍 [開始剖析 PE 結構] 目標檔案: {filepath}")
    surgeon = PESurgeon(filepath)
    print(f"   ➔ 架構類型: {'64-bit (x64 / PE32+)' if surgeon.is_64bit else '32-bit (x86 / PE32)'}")
    print(f"   ➔ PE 區段 (Sections) 數量: {len(surgeon.sections)}")
    for sec in surgeon.sections:
        print(f"      • {sec['name']:<8} RVA: 0x{sec['vaddr']:08X} (大小: {sec['vsize']} bytes)")

    print("\n📦 [導入表 (IAT) 檢視與危險 API 掃描]:")
    imports = surgeon.scan_imports()
    threat_count = 0
    for dll in imports:
        print(f"\n   📁 依賴模組: {dll['dll']}")
        for fn in dll['functions']:
            if fn['name'] in surgeon.DANGEROUS_API_MAPPINGS:
                threat_count += 1
                replacement = surgeon.DANGEROUS_API_MAPPINGS[fn['name']].replace('\0', '')
                print(f"      🚨 [危險 API 標靶] {fn['name']:<24} (檔案位移: 0x{fn['name_offset']:X})")
                print(f"         ➔ 可置換對策: 置換為「{replacement}」中和呼叫")
            else:
                # Truncate normal APIs so console isn't flooded
                pass
        # Show count of benign APIs
        normal_count = len(dll['functions'])
        print(f"      └─ 總計導入 {normal_count} 個函數。")

    print("\n" + "="*63)
    if threat_count > 0:
        print(f"⚠️ 發現 {threat_count} 個可被外科手術洗白的破壞性 API！")
        print("💡 可使用指令進行中和補丁: python slime_surgeon.py patch <檔案路徑>")
    else:
        print("✅ 未發現常見破壞性 API 標靶，或該檔案已為乾淨狀態。")
    print("="*63 + "\n")

def patch_binary(filepath: str, output_path: str = None):
    print(BANNER)
    src = Path(filepath)
    if not output_path:
        output_path = str(src.parent / f"tamed_{src.name}")

    print(f"💉 [開始執行 IAT 外科手術] 來源目標: {src.name}")
    surgeon = PESurgeon(str(src))
    result = surgeon.apply_surgical_patch(output_path)

    print("\n" + "="*63)
    if result["total_threats_neutralized"] > 0:
        print(f"🎉 [手術成功] 已中和 {result['total_threats_neutralized']} 個危險 API 呼叫點！")
        for act in result["details"]:
            print(f"   • [{act['dll']}] {act['original_api']} ➔ 置換為 ➔ {act['neutralized_with']}")
            print(f"     (檔案位移: {act['file_offset']})")
        print(f"\n📦 新生安全執行檔已輸出至: {result['patched_file']}")
        print("🛡️ 當此程式執行時，任何試圖破壞系統的呼叫將安全地被重定向至無害查詢！")
    else:
        print("ℹ️ 該二進制檔案中未找到需要置換的目標 API。")
    print("="*63 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Slime PE Surgeon")
    subparsers = parser.add_subparsers(dest="command")

    inspect_p = subparsers.add_parser("inspect", help="剖析 PE 結構與掃描 IAT 危險 API")
    inspect_p.add_argument("file", help="目標 .exe 或 .dll 檔案路徑")

    patch_p = subparsers.add_parser("patch", help="對 PE 檔案執行 IAT 外科手術補丁")
    patch_p.add_argument("file", help="目標 .exe 或 .dll 檔案路徑")
    patch_p.add_argument("-o", "--output", default=None, help="補丁後輸出路徑")

    args = parser.parse_args()
    if args.command == "inspect":
        inspect_binary(args.file)
    elif args.command == "patch":
        patch_binary(args.file, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
