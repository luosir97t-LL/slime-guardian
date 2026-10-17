@echo off
chcp 65001 > nul
title 史萊姆全方位守護中心 (Slime Guardian Center)
cls

echo ====================================================================
echo           🟢 史萊姆再生與守護中心 (SLIME GUARDIAN v2.0)
echo ====================================================================
echo.
echo [1] 執行全系統六大支柱完整性自我檢驗 (Self-Diagnostic)
echo [2] 盤查本機電腦安全與 Gmail 通行證保護狀態 (Scan PC)
echo [3] 測試 AI Agent 侵入防禦迷宮 (Honey-Matrix)
echo [4] 測試 AI 擬真釣魚與詐騙信嗅覺 (Phishing Sniffer)
echo [5] 檢視太極陰陽中和矩陣 (Tai Chi Matrix)
echo [6] 檢視 100%% 離線無雲自體防禦狀態 (Offline Mode)
echo [0] 離開
echo.
echo ====================================================================
set /p opt="請輸入選項 [1-6, 0]: "

if "%opt%"=="1" (
    python test_all_subsystems.py
    pause
    goto :eof
)
if "%opt%"=="2" (
    python slime_guardian.py scan-pc
    pause
    goto :eof
)
if "%opt%"=="3" (
    python slime_guardian.py test-agent
    pause
    goto :eof
)
if "%opt%"=="4" (
    python slime_guardian.py test-phishing
    pause
    goto :eof
)
if "%opt%"=="5" (
    python slime_guardian.py taichi
    pause
    goto :eof
)
if "%opt%"=="6" (
    python slime_guardian.py offline
    pause
    goto :eof
)
if "%opt%"=="0" exit
