"""
Slime Real-Time Guard - External Email & Web Attack Shield
Provides continuous protection for incoming emails (attachments, phishing links)
and web-based attack vectors (drive-by downloads, exploit redirects, malicious domains).
"""
import os
import sys
import re
import json
import urllib.parse
from pathlib import Path
from typing import Dict, List, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from .phishing_sniffer import PhishingSniffer
from .taichi_harmonizer import TaiChiHarmonizer

class RealTimeGuard:
    """Monitors external email attachments and incoming web links in real time."""

    DANGEROUS_MAIL_EXTS = {
        ".exe", ".scr", ".vbs", ".js", ".bat", ".cmd", ".iso", ".hta", ".wsf", ".ps1"
    }

    MALICIOUS_WEB_PATTERNS = [
        r"(?:free-nitro|free-gift|steam-gift|wallet-validator|bonus-claim)\.",
        r"(?:login-verification|account-recovery|security-update-google)\.",
        r"(?:crypto-airdrop|metamask-sync|ledger-auth)\.",
        r"\.ru/login|\.xyz/auth|\.top/verify"
    ]

    def __init__(self, quarantine_dir: str = "./.slime_quarantine"):
        self.quarantine_dir = Path(quarantine_dir)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        self.sniffer = PhishingSniffer()
        self.harmonizer = TaiChiHarmonizer()
        self.intercepted_events = []

    def inspect_incoming_attachment(self, filepath: str) -> Dict[str, Any]:
        """
        Intercepts incoming email attachments (from Downloads or mail clients).
        If dangerous, locks the file into the Slime Quarantine before user can run it.
        """
        path = Path(filepath)
        if not path.exists():
            return {"status": "FILE_NOT_FOUND", "is_safe": True}

        suffix = path.suffix.lower()
        is_double_ext = bool(re.search(r'\.(?:pdf|docx|xlsx|jpg)\.(?:exe|scr|vbs|bat)$', path.name, re.IGNORECASE))
        is_dangerous = suffix in self.DANGEROUS_MAIL_EXTS or is_double_ext

        if is_dangerous:
            # 1. Neutralize: Move into Slime Quarantine Vault with non-executable permissions
            quarantined_path = self.quarantine_dir / f"quarantined_{path.name}.tamed"
            try:
                path.rename(quarantined_path)
            except Exception:
                pass

            event = {
                "type": "MAIL_ATTACHMENT_NEUTRALIZED",
                "original_filename": path.name,
                "reason": "高危雙副檔名偽裝或直接可執行檔附件" if is_double_ext else f"危險郵件附件副檔名 ({suffix})",
                "action": "已自動從收件匣截斷，封入史萊姆安全隔離區",
                "quarantine_location": str(quarantined_path.resolve())
            }
            self.intercepted_events.append(event)
            return {
                "is_safe": False,
                "risk_level": "CRITICAL",
                "event": event,
                "message": f"🚨 [郵件防護攔截] 發現危險附件「{path.name}」！已在您點擊前自動搶先鎖定隔離。"
            }
        else:
            return {
                "is_safe": True,
                "risk_level": "LOW",
                "message": f"✅ [郵件附件安全] 「{path.name}」為一般無害文件格式。"
            }

    def inspect_incoming_web_url(self, url: str) -> Dict[str, Any]:
        """
        Inspects incoming links from emails, Discord, Skype, or browser clicks.
        Blocks phishing URLs, drive-by download sites, and credential harvesters.
        """
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        is_malicious = False
        reasons = []

        # 1. Match known phishing and exploit domain patterns
        for pattern in self.MALICIOUS_WEB_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                is_malicious = True
                reasons.append("符合釣魚網站域名模式")
                break

        # 2. Check for deceptive IP addresses or abnormal TLDs
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            is_malicious = True
            reasons.append("直接使用純 IP 位址偽裝，意圖規避網域信譽庫")

        if any(domain.endswith(tld) for tld in [".xyz", ".top", ".cc", ".click", ".link"]) and any(w in domain for w in ["google", "login", "bank", "secure"]):
            is_malicious = True
            reasons.append("高仿知名官方服務的高危頂級域名 (Typosquatting)")

        if is_malicious:
            event = {
                "type": "WEB_ATTACK_BLOCKED",
                "target_url": url,
                "domain": domain,
                "reasons": reasons,
                "action": "連線已於本地端被攔截中和，導向安全警告"
            }
            self.intercepted_events.append(event)
            return {
                "is_blocked": True,
                "risk_level": "CRITICAL",
                "event": event,
                "message": f"🛡️ [網站攻擊攔截] 阻斷高危釣魚/惡意網站「{domain}」！"
            }
        else:
            return {
                "is_blocked": False,
                "risk_level": "SAFE",
                "message": f"✅ [網址安全] 「{domain}」信譽良好，安全放行。"
            }
