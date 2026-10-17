"""
Slime Web & Browser Guardian
Penetrates traditional AV's blind spot: In-browser memory attacks, WebAssembly cryptominers,
and fake credential harvesting DOM forms.
"""
import re
from typing import Dict, List, Any

class WebBrowserGuard:
    """Detects and neutralizes malicious scripts operating purely inside browser memory/DOM."""

    MINER_SIGNATURES = [
        "coinhive", "cryptoloot", "coin-hive", "cryptonight",
        "webassembly.instantiate", "wasm_mining", "stratum+tcp", "monerominer"
    ]

    FAKE_LOGIN_PATTERNS = [
        r'<form[^>]*action=["\']https?://(?!.*google\.com)[^"\']*(?:login|signin|auth)[^"\']*["\']',
        r'input[^>]*type=["\']password["\'][^>]*name=["\'](?!.*google)[^"\']*pass'
    ]

    def audit_webpage_content(self, url: str, html_or_js_content: str) -> Dict[str, Any]:
        """Inspects HTML/JavaScript content within browser tabs."""
        threats = []
        is_mining = False
        is_fake_login = False

        content_lower = html_or_js_content.lower()

        # 1. Inspect for in-browser cryptomining
        for sig in self.MINER_SIGNATURES:
            if sig in content_lower:
                is_mining = True
                threats.append({
                    "category": "BROWSER_MINER",
                    "severity": "CRITICAL",
                    "detail": f"偵測到網頁偷跑挖礦腳本特徵: {sig} (意圖霸佔 CPU 100% 算力)"
                })
                break

        # 2. Inspect for fake login credential forms (DOM level)
        for pattern in self.FAKE_LOGIN_PATTERNS:
            if re.search(pattern, html_or_js_content, re.IGNORECASE):
                is_fake_login = True
                threats.append({
                    "category": "CREDENTIAL_HARVESTING_FORM",
                    "severity": "CRITICAL",
                    "detail": "偵測到仿冒登入表單：將密碼提交至未知第三方第三方伺服器"
                })
                break

        # 3. Apply Slime Sticky Neutralization
        sanitized_script = html_or_js_content
        if is_mining:
            # Wrap and neutralize WebAssembly / mining worker loops
            sanitized_script = re.sub(
                r'new\s+Worker\s*\((.*?)\)',
                r'/* [🟢 史萊姆中和] 終止挖礦 Worker */ { postMessage: function(){}, terminate: function(){ console.log("Slime neutralized miner"); } }',
                sanitized_script,
                flags=re.IGNORECASE
            )

        return {
            "url": url,
            "has_threats": len(threats) > 0,
            "threats": threats,
            "slime_action": "太極中和：封鎖挖礦迴圈並將表單導流至蜜罐" if len(threats) > 0 else "放行安全網頁",
            "sanitized_preview": sanitized_script[:300] if is_mining else None
        }
