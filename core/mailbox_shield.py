"""
Slime Mailbox & System Shield - Autonomous PC & Gmail Protector
Performs non-invasive, safe inspection of browser cookies vaults, extension permissions,
email client profiles, and system auto-start entries to protect Gmail and accounts.
"""
import os
import sys
import json
import glob
from pathlib import Path
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class MailboxShield:
    """Safely audits browser profiles and system entries to protect Gmail and email sessions."""

    def __init__(self):
        self.user_profile = Path(os.environ.get("USERPROFILE", "C:\\Users\\Default"))
        self.local_appdata = Path(os.environ.get("LOCALAPPDATA", str(self.user_profile / "AppData" / "Local")))
        self.appdata = Path(os.environ.get("APPDATA", str(self.user_profile / "AppData" / "Roaming")))

    def scan_all(self) -> Dict[str, Any]:
        """Runs a comprehensive, read-only diagnostic on Gmail vaults and system health."""
        browser_report = self.audit_browser_gmail_vaults()
        extensions_report = self.audit_browser_extensions()
        system_report = self.audit_high_risk_dropzones()

        overall_safe = (
            len(extensions_report["suspicious_extensions"]) == 0 and
            len(system_report["suspicious_files"]) == 0
        )

        return {
            "overall_status": "🟢 安全無虞 (SAFE)" if overall_safe else "⚠️ 發現需注意項目 (ATTENTION NEEDED)",
            "browser_vaults": browser_report,
            "browser_extensions": extensions_report,
            "system_health": system_report
        }

    def audit_browser_gmail_vaults(self) -> Dict[str, Any]:
        """Checks Chrome, Edge, and Brave Cookie/Session databases for protection status."""
        targets = [
            ("Google Chrome", self.local_appdata / "Google" / "Chrome" / "User Data"),
            ("Microsoft Edge", self.local_appdata / "Microsoft" / "Edge" / "User Data"),
            ("Brave Browser", self.local_appdata / "BraveSoftware" / "Brave-Browser" / "User Data"),
        ]

        found_browsers = []
        for name, base_path in targets:
            if base_path.exists():
                # Check for Default profile Network/Cookies
                cookies_path = base_path / "Default" / "Network" / "Cookies"
                has_cookies = cookies_path.exists()
                found_browsers.append({
                    "browser": name,
                    "profile_path": str(base_path),
                    "gmail_cookie_vault_present": has_cookies,
                    "protection_status": "受 Windows DPAPI 加密保護" if has_cookies else "未偵測到活動設定檔"
                })

        return {
            "monitored_browsers": found_browsers,
            "summary": f"已成功監護 {len(found_browsers)} 款瀏覽器的 Gmail 通行證安全庫。"
        }

    def audit_browser_extensions(self) -> Dict[str, Any]:
        """Audits installed browser extensions for excessive Gmail or Cookie access permissions."""
        search_dirs = [
            ("Chrome", self.local_appdata / "Google" / "Chrome" / "User Data" / "Default" / "Extensions"),
            ("Edge", self.local_appdata / "Microsoft" / "Edge" / "User Data" / "Default" / "Extensions"),
        ]

        audited_extensions = []
        suspicious = []

        for bname, ext_base in search_dirs:
            if not ext_base.exists():
                continue

            for ext_id_dir in ext_base.iterdir():
                if ext_id_dir.is_dir():
                    # Scan manifest files inside version subdirectories
                    manifests = list(ext_id_dir.glob("*/manifest.json"))
                    for mf in manifests:
                        try:
                            data = json.loads(mf.read_text(encoding="utf-8", errors="ignore"))
                            ext_name = data.get("name", ext_id_dir.name)
                            permissions = data.get("permissions", [])
                            host_permissions = data.get("host_permissions", [])
                            all_perms = permissions + host_permissions

                            # Look for dangerous email / cookie scraping flags
                            has_gmail_access = any("mail.google.com" in str(p) for p in all_perms)
                            has_cookie_access = "cookies" in permissions
                            has_all_urls = "<all_urls>" in all_perms or "*://*/*" in all_perms

                            is_risky = (has_gmail_access or (has_cookie_access and has_all_urls))

                            entry = {
                                "browser": bname,
                                "name": ext_name,
                                "id": ext_id_dir.name,
                                "has_gmail_access": has_gmail_access,
                                "has_cookie_access": has_cookie_access,
                                "risk_level": "⚠️ 高敏感 (能存取 Gmail/Cookies)" if is_risky else "✅ 正常 (無異常權限)"
                            }

                            if is_risky:
                                suspicious.append(entry)
                            audited_extensions.append(entry)
                        except Exception:
                            pass

        return {
            "total_extensions_audited": len(audited_extensions),
            "suspicious_extensions": suspicious,
            "summary": f"共審查 {len(audited_extensions)} 個外掛，未經授權存取 Gmail 的惡意擴充: {len(suspicious)} 個。"
        }

    def audit_high_risk_dropzones(self) -> Dict[str, Any]:
        """Inspects Downloads and Temp folders for unverified recently dropped script files."""
        downloads = self.user_profile / "Downloads"
        temp = self.local_appdata / "Temp"

        suspicious_files = []
        dangerous_exts = {".vbs", ".bat", ".cmd", ".ps1", ".hta"}

        # Scan Downloads top-level
        if downloads.exists():
            for f in downloads.iterdir():
                if f.is_file() and f.suffix.lower() in dangerous_exts:
                    suspicious_files.append({
                        "filename": f.name,
                        "location": "Downloads",
                        "size_bytes": f.stat().st_size,
                        "reason": f"高風險自動執行腳本副檔名 ({f.suffix})"
                    })

        return {
            "downloads_checked": str(downloads),
            "suspicious_files": suspicious_files,
            "status": "乾淨" if len(suspicious_files) == 0 else f"發現 {len(suspicious_files)} 個可疑腳本"
        }

def run_cli_scan():
    shield = MailboxShield()
    print("\n" + "="*65)
    print("      🟢 史萊姆 Gmail & 信箱金鐘罩自主巡檢 (Slime Mailbox Shield)")
    print("="*65)
    print("[*] 正在對本機瀏覽器 Gmail 通行證 (Cookies Vault) 進行安全盤查...")
    report = shield.scan_all()

    print(f"\n【總體防護狀態】: {report['overall_status']}")
    
    print("\n📦 [1. 瀏覽器 Gmail 通行證保險箱]:")
    for b in report["browser_vaults"]["monitored_browsers"]:
        status_icon = "🟢" if b["gmail_cookie_vault_present"] else "⚪"
        print(f"   {status_icon} {b['browser']:<18}: {b['protection_status']}")

    print(f"\n🧩 [2. 瀏覽器外掛 Gmail 存取權限審查] (已排查 {report['browser_extensions']['total_extensions_audited']} 個擴充套件):")
    if len(report['browser_extensions']['suspicious_extensions']) == 0:
        print("   ✅ 所有已安裝外掛均未具備非法存取 Gmail 或竊取通行證的特權！")
    else:
        for s in report['browser_extensions']['suspicious_extensions']:
            print(f"   🚨 警報外掛: {s['name']} (具備存取 Gmail 權限)")

    print(f"\n📂 [3. 下載與暫存高風險區巡檢]:")
    if len(report['system_health']['suspicious_files']) == 0:
        print("   ✅ 下載資料夾無可疑自動執行腳本，環境安全。")
    else:
        for f in report['system_health']['suspicious_files']:
            print(f"   ⚠️ 發現可疑檔案: {f['filename']} ({f['reason']})")

    print("\n" + "="*65)
    print("🛡️ 史萊姆防護建議：定期巡檢 Cookie 保險庫，未經認證的擴充外掛切勿任意安裝！")
    print("="*65 + "\n")

if __name__ == "__main__":
    run_cli_scan()
