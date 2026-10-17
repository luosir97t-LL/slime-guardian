# 🌐 史萊姆「外網雲端拋棄式靶場」操作指南

> **零本機風險保證**：所有的測試、模擬與二進制手術，全都在**微軟海外資料中心的雲端伺服器（Azure VM）**上進行。測試完成後該虛擬機立即自動銷毀，你的個人電腦不需要執行任何測試代碼！

---

## 🚀 三步啟動外網雲端測試

### 第一步：在 GitHub 建立一個倉庫 (Repository)
1. 打開瀏覽器，前往 [github.com](https://github.com/)（如果還沒有帳號可免費註冊一個）。
2. 點擊右上角的 **「+」** ➔ 選擇 **「New repository」**。
3. 倉庫名稱填入：`slime-guardian`。
4. 可以選擇 **Private（私有）** 或 **Public（公開）**，然後點擊 **「Create repository」**。

---

### 第二步：將本專案上傳至 GitHub
你有兩種最簡單的上傳方式：

#### 方式 A：直接在 GitHub 網頁上傳（最簡單，免打指令）
1. 在剛建立好的 GitHub 倉庫頁面，點擊 **「uploading an existing file」**。
2. 將本專案資料夾內的所有檔案直接拖曳進瀏覽器：
   - 路徑：`C:\Users\karas\.gemini\antigravity\scratch\slime-transmutation-engine`
3. 點擊下方的綠色按鈕 **「Commit changes」** 完成上傳。

#### 方式 B：使用 Git 指令推送
在終端機中執行：
```powershell
cd C:\Users\karas\.gemini\antigravity\scratch\slime-transmutation-engine
git init
git add .
git commit -m "Deploy Slime Guardian Engine"
git branch -M main
git remote add origin https://github.com/<你的使用者名稱>/slime-guardian.git
git push -u origin main
```

---

### 第三步：在 GitHub 網頁一鍵觸發外網雲端測試！

1. 打開你的 GitHub 倉庫頁面，點擊頂部的 **「Actions」** 分頁。
2. 在左側選單會看到 **「🟢 史萊姆雲端拋棄式靶場測試」**。
3. 點擊右側的 **「Run workflow」** 按鈕 ➔ 點擊綠色的 **「Run workflow」**。
4. **見證奇蹟**：
   - 微軟 Azure 會在外網機房立刻啟動一台全新的 Windows 雲端電腦。
   - 你可以在網頁上**即時看到雲端執行的彩色日誌**（AI 釣魚嗅覺、惡意 Agent 迷宮、二進制手術）。
   - 執行完畢後，微軟會自動銷毀該雲端伺服器，並把測試產生的安全報告打包供你下載！

---

## 🔒 為什麼外網雲端測試是 100% 安全的？

| 指標 | 本機測試 | 🌐 GitHub 雲端靶場測試 |
| :--- | :--- | :--- |
| **執行地點** | 你的個人電腦 CPU / 記憶體 | **微軟海外 Azure 資料中心雲端主機** |
| **硬碟接觸** | 本機 SSD / HDD | **拋棄式虛擬硬碟（Ephemeral Disk）** |
| **測試完畢處置** | 本機自動刪除暫存檔 | **整台雲端虛擬機由微軟直接徹底銷毀抹除** |
| **本機中毒風險** | 0% (使用純模擬假資料) | **物理級絕對隔離 0% (連網路封包都沒經過你家)** |
