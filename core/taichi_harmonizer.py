"""
Slime Tai Chi Harmonizer - The Yin-Yang Neutralization Matrix
Implements the philosophy:
"世上一凹一凸，組合成圓。若病毒是太極之黑，史萊姆便是太極之白，
不與其同歸於盡，而是包覆中和，將破壞力轉化為守護力，化為圓滿太極。"
"""
from typing import Dict, Any, List

class TaiChiHarmonizer:
    """Translates 'Dark' destructive vectors into their exact 'White' constructive complements."""

    TAICHI_MATRIX = {
        # 1. 勒索加密 (Black) ➔ 離線備份金鑰庫 (White)
        "RANSOMWARE": {
            "black_element": "非對稱勒索加密 (強奪控制權)",
            "white_complement": "自定義保護金鑰備份 (自主控制權)",
            "harmonized_circle": "🛡️ 太極・自主離線加密保險箱 (AES Vault)",
            "philosophy": "你欲奪之，我反予使用者完全掌控；以自主備份化解惡意勒索。"
        },
        # 2. 磁碟抹除 (Black) ➔ 零破壞隔離清理 (White)
        "FILE_WIPER": {
            "black_element": "永久摧毀本地檔案 (不可逆抹除)",
            "white_complement": "可隨時還原之安全隔離艙 (可逆保存)",
            "harmonized_circle": "🛡️ 太極・時光回溯防護清理器 (Rollback Cleaner)",
            "philosophy": "你欲毀之，我反將其妥善封存；以永恆備存化解虛無毀滅。"
        },
        # 3. 憑證竊密 (Black) ➔ 本機隱私漏洞雷達 (White)
        "DATA_EXFILTRATION": {
            "black_element": "偷窺並向外部 C2 外傳隱私 (刺探與洩密)",
            "white_complement": "本地外連安全監聽與截流 (截斷與診斷)",
            "harmonized_circle": "🛡️ 太極・私有網路流量體檢器 (Traffic Inspector)",
            "philosophy": "你欲竊之，我反以此洞悉系統軟肋；以主動診斷化解暗處偷襲。"
        },
        # 4. 網頁挖礦 (Black) ➔ 系統硬體節能優化 (White)
        "BROWSER_MINER": {
            "black_element": "竊佔 CPU/GPU 算力瘋狂挖礦 (高耗能壓榨)",
            "white_complement": "進程節能限制與背景閒置休眠 (極低耗能休眠)",
            "harmonized_circle": "🛡️ 太極・綠色硬體降溫節能器 (Green Eco Optimizer)",
            "philosophy": "你欲耗之，我反以靜制動；以深層休眠化解狂暴壓榨。"
        },
        # 5. 物聯網殭屍跳板 (Black) ➔ 智慧家庭蜜罐雷達 (White)
        "IOT_BOTNET": {
            "black_element": "掃描脆弱連接埠劫持設備 (無孔不入擴散)",
            "white_complement": "虛擬誘捕節點引導流量 (固若金湯吸收)",
            "harmonized_circle": "🛡️ 太極・智慧家庭安全感測雷達 (Home IoT Sentry)",
            "philosophy": "你欲攻之，我反設虛景相迎；以虛擬夢境化解實體侵略。"
        }
    }

    def harmonize(self, threat_type: str) -> Dict[str, Any]:
        """Calculates the complementary White force for any Dark threat."""
        threat_key = threat_type.upper()
        if threat_key in self.TAICHI_MATRIX:
            return self.TAICHI_MATRIX[threat_key]
        
        # Default generic Tai Chi harmonization
        return {
            "black_element": f"未知破壞性行為 ({threat_type})",
            "white_complement": "史萊姆黏性包覆與語意重組",
            "harmonized_circle": "🛡️ 太極・自適應防衛結晶工具",
            "philosophy": "萬物負陰而抱陽，中氣以為和。任何破壞力皆能轉化為建設力。"
        }
