"""
Slime Phishing Sniffer - AI Social Engineering & Mailbox Guardian
Analyzes email text, sender domains, and attachments for AI-generated phishing,
lookalike domains, urgency manipulation, and credential harvesting hooks.
"""
import re
from typing import Dict, List, Any
from urllib.parse import urlparse

class PhishingSniffer:
    """Detects AI-crafted spear phishing, fake Gmail security alerts, and deceptive links."""

    URGENCY_KEYWORDS = [
        "24小時內", "即將凍結", "立即驗證", "最後通牒", "帳號異常", "緊急處理",
        "立即更新密碼", "安全警告", "帳單逾期", "立即匯款", "點擊此處解鎖",
        "urgent", "suspended", "verify your account", "immediate action required"
    ]

    DECEPTIVE_TLDS = [".xyz", ".top", ".cc", ".ru", ".tk", ".work", ".click", ".live"]

    LEGITIMATE_GMAIL_DOMAINS = ["google.com", "gmail.com", "accounts.google.com"]

    def analyze_email(self, sender: str, subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
        attachments = attachments or []
        risk_score = 0
        detected_indicators = []

        # 1. Analyze Sender Impersonation (including lookalike typosquatting)
        is_impersonating_google = (
            any(brand in sender.lower() for brand in ["google", "gmail", "security-alert", "service-team"]) or
            bool(re.search(r"g[o0]{2}g[l1]e|gm[a4]il", sender.lower()))
        )
        sender_domain = sender.split("@")[-1].strip().lower() if "@" in sender else sender.lower()

        if is_impersonating_google and sender_domain not in self.LEGITIMATE_GMAIL_DOMAINS:
            risk_score += 45
            detected_indicators.append({
                "type": "BRAND_IMPERSONATION",
                "severity": "CRITICAL",
                "detail": f"發件人假冒 Google 官方團隊，但實際網域為非官方域名「{sender_domain}」"
            })

        # 2. Analyze Psychological Urgency / Pressure
        urgency_matches = [kw for kw in self.URGENCY_KEYWORDS if kw in subject or kw in body]
        if urgency_matches:
            risk_score += min(30, len(urgency_matches) * 12)
            detected_indicators.append({
                "type": "PSYCHOLOGICAL_URGENCY",
                "severity": "HIGH",
                "detail": f"偵測到 AI 慣用的焦慮施壓詞彙: {', '.join(urgency_matches[:3])}"
            })

        # 3. Analyze Embedded Links
        extracted_urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)
        suspicious_urls = []
        for url in extracted_urls:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if any(domain.endswith(tld) for tld in self.DECEPTIVE_TLDS):
                suspicious_urls.append(url)
            elif is_impersonating_google and "google.com" not in domain:
                suspicious_urls.append(url)

        if suspicious_urls:
            risk_score += 35
            detected_indicators.append({
                "type": "CREDENTIAL_HARVESTING_LINK",
                "severity": "CRITICAL",
                "detail": f"郵件包含偽裝的釣魚表單或高危網址: {suspicious_urls[0]}"
            })

        # 4. Analyze Dangerous Attachments
        for att in attachments:
            ext = att.lower().split(".")[-1]
            if ext in ["exe", "scr", "vbs", "bat", "iso", "hta"] or ".pdf.exe" in att.lower():
                risk_score += 50
                detected_indicators.append({
                    "type": "DANGEROUS_PAYLOAD_ATTACHMENT",
                    "severity": "CRITICAL",
                    "detail": f"包含高危偽裝執行檔附件: {att}"
                })

        risk_score = min(100, risk_score)
        is_phishing = risk_score >= 50

        return {
            "is_phishing": is_phishing,
            "risk_score": risk_score,
            "threat_verdict": "🚨 高危 AI 釣魚詐騙信件" if is_phishing else ("⚠️ 具疑慮但可能良性" if risk_score > 25 else "✅ 正常安全郵件"),
            "detected_indicators": detected_indicators,
            "recommended_action": "將發件人與釣魚連結直接打入【無限夢境】隔離" if is_phishing else "正常閱覽",
            "extracted_urls": extracted_urls
        }
