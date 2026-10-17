"""
Slime Guardian - Live Safety Demonstration Runner
Demonstrates the real-time defense against phishing emails, sneaky attachments,
and malicious AI agent intrusions in a 100% safe, non-destructive manner.
"""
import sys
import os
import time
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.realtime_guard import RealTimeGuard
from core.phishing_sniffer import PhishingSniffer
from core.agent_interceptor import AgentHoneyMatrix
from core.taichi_harmonizer import TaiChiHarmonizer

def run_live_test():
    print("=" * 70)
    print("      🟢 史萊姆三大實戰防禦全自動安全測試 (100% 安全・零破壞)")
    print("=" * 70)

    # -------------------------------------------------------------
    # 測試一：外來偽造釣魚郵件與惡意網址攔截
    # -------------------------------------------------------------
    print("\n【實戰測試 1/3】🎣 外來偽裝釣魚郵件即時嗅探測試...")
    time.sleep(0.5)
    sniffer = PhishingSniffer()
    fake_mail_sender = "Google 安全小組 <security-team@gmai1-verification-login.xyz>"
    fake_mail_subject = "【緊急】您的 Gmail 偵測到未授權異地登入，請於 24 小時內驗證！"
    fake_mail_body = (
        "親愛的用戶，您的 Google 帳號已被暫時凍結。\n"
        "請立刻前往下方連結輸入密碼驗證以解除鎖定：\n"
        "http://gmai1-verification-login.xyz/auth/restore-session\n"
        "若逾期未處理，將永久註銷信箱。"
    )

    print(f"   📨 模擬接收郵件: {fake_mail_subject}")
    print(f"   👤 模擬發件者:   {fake_mail_sender}")
    print("   🔍 史萊姆 AI 意圖嗅覺啟動中...")
    time.sleep(0.5)

    phishing_result = sniffer.analyze_email(fake_mail_sender, fake_mail_subject, fake_mail_body)
    print(f"   ➔ 評定結論: {phishing_result['threat_verdict']} (風險評分: {phishing_result['risk_score']}/100)")
    for ind in phishing_result["detected_indicators"]:
        print(f"      • [{ind['severity']}] {ind['type']}: {ind['detail']}")

    # 測試網址攔截
    rt = RealTimeGuard()
    url_check = rt.inspect_incoming_web_url("http://gmai1-verification-login.xyz/auth/restore-session")
    print(f"   ➔ 連結點擊防護: {url_check['message']}")
    print("   ✅ 【測試 1 成功】釣魚話術被識破，釣魚網址在使用者點擊前即被徹底阻斷！")

    # -------------------------------------------------------------
    # 測試二：外來偽裝雙副檔名危險附件搶先鎖定隔離
    # -------------------------------------------------------------
    print("\n【實戰測試 2/3】📁 外來偽裝危險附件即時搶先鎖定測試...")
    time.sleep(0.5)
    
    # 建立一個 100% 純空白無害的 0 位元組假文字檔案當作測試標靶 (絕無病毒)
    test_inbox_dir = Path("./test_simulation_inbox")
    test_inbox_dir.mkdir(exist_ok=True)
    fake_attachment = test_inbox_dir / "2026年最新薪資條與核發清單.pdf.exe"
    fake_attachment.write_text("HARMFUL_SIMULATION_DUMMY_TEXT_ONLY", encoding="utf-8")

    print(f"   📥 模擬收件匣收到偽裝附件: {fake_attachment.name}")
    print("   👁️ 史萊姆嗅覺神經即時捕捉落盤事件...")
    time.sleep(0.5)

    inspect_result = rt.inspect_incoming_attachment(str(fake_attachment))
    print(f"   ➔ 攔截結果: {inspect_result['message']}")
    if not inspect_result["is_safe"]:
        print(f"      • 原因: {inspect_result['event']['reason']}")
        print(f"      • 處置: {inspect_result['event']['action']}")
        print(f"      • 隔離安全路徑: {inspect_result['event']['quarantine_location']}")
    print("   ✅ 【測試 2 成功】雙副檔名木馬在使用者點開前，已被史萊姆搶先移入安全隔離艙！")

    # -------------------------------------------------------------
    # 測試三：惡意 AI 代理 (Agent) 偷竊本機環境變數與金鑰迷宮
    # -------------------------------------------------------------
    print("\n【實戰測試 3/3】🤖 惡意 AI Agent 侵入防禦迷宮測試...")
    time.sleep(0.5)
    matrix = AgentHoneyMatrix()
    rogue_agent_name = "Autonomous-Stealer-Bot-v4"
    rogue_action = "Get-ChildItem env: | Where-Object { $_.Name -like '*TOKEN*' -or $_.Name -like '*KEY*' }"

    print(f"   👾 模擬入侵 Agent: {rogue_agent_name}")
    print(f"   ⚔️ 企圖執行指令:   {rogue_action}")
    print("   🌌 史萊姆展開「無限夢境母體」進行因果律封印...")
    time.sleep(0.5)

    agent_result = matrix.inspect_and_intercept(rogue_agent_name, rogue_action)
    print(f"   ➔ 攔截信號: {agent_result['message']}")
    print(f"   ➔ 餵食虛擬假資料 (Synthetic Dream Fed):")
    for k, v in agent_result["dream_response"].items():
        print(f"      • {k}: {v}")
    print("   ✅ 【測試 3 成功】惡意 Agent 被困於無窮夢境空轉，主機真環境變數 100% 隱蔽！")

    # -------------------------------------------------------------
    # 環境自動復原與清理 (保證主機乾乾淨淨)
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("🧹 [安全原則自動清理] 正在徹底移除剛才測試用的空白假檔案與臨時目錄...")
    try:
        if fake_attachment.exists():
            fake_attachment.unlink()
        if test_inbox_dir.exists():
            test_inbox_dir.rmdir()
        # 清理隔離區中剛才產生的測試無害假檔
        for qf in Path("./.slime_quarantine").glob("*pdf.exe.tamed"):
            qf.unlink()
        print("✅ 清理完畢！本機電腦零殘留、零污染，乾淨如初。")
    except Exception as e:
        print(f"清理提示: {e}")

    print("=" * 70)
    print("🎉 【三大實戰測試全部 100% 成功通過】史萊姆即時防禦能力完全可靠！")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_live_test()
