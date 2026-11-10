# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（L3）。

## ⏯️ 目前做到哪
康軒國小健體六上・單元一「健康用網路」第 1 課「網路不沉迷」：教材＋網頁＋對戰全部完成並通過驗收（verify_site.js 36/36 全過、瀏覽器 0 console error），尚未 git commit 完成與上線。

## 🚦 目前狀態
| 項目 | 狀態 |
|------|------|
| 教案 docx | ✅ 教案/教案_網路不沉迷.docx（officecli validate 0 錯誤） |
| 教學簡報 pptx | ✅ 簡報/網路不沉迷_教學簡報.pptx（22 頁 16:9，JPG 已匯出） |
| 學習單 | ✅ 學習單 1（篩檢＋作息）、學習單 2（規範＋我訊息） |
| 測驗卷 | ✅ docx＋PDF（Word COM 轉檔） |
| 旁白動畫 | ✅ p09/p12/p16/p18.mp4（1920×1080、12–15 秒、有音訊） |
| 教學網頁 | ✅ index.html（map/labs/deck/quiz/videos/tools/battle/gallery/downloads 全齊） |
| 對戰 | ✅ battle.html＋server.js＋questions.json 30 題 |
| 素材圖庫 | ✅ media/images.js 22 筆（Pillow 程式繪圖，非 AI 生圖） |
| GitHub Pages | ⏳ 待使用者授權後建 repo 部署 |
| Render 對戰後端 | ⏳ 待使用者授權 |

## 🔗 網址
- 首頁：（部署後填）
- 對戰頁：（部署後填）
- repo：（建立後填）

## 📌 重要修正紀錄
- 封面確認是**國小**六上（不是國中九上）；節數照官方課程計畫是 **3 節×40 分**。
- 簡報是 **22 頁**（不是模板寫的 21 頁），動畫頁＝p09/p12/p16/p18。
- GEMINI_API_KEY 未設定 → 圖庫改用 Pillow 繪製概念卡（工具/build_gallery.py）。
- 對戰答案分布確定性重排為 0:7／1:8／2:8／3:7（content.py 末端）。
- docx 標題勿加 w:pBdr（OOXML 順序違規，officecli validate 會報錯）。
- edge-tts 用 `--rate=+10%`；ffprobe subprocess 要指定 encoding="utf-8"。
- 測驗卷 PDF 用 Word COM（PowerShell 腳本 docx_to_pdf.ps1），不用 LibreOffice。
- Windows 終端中文亂碼是顯示問題；多行 Python 用 .py 檔執行，不要內嵌。

## ➡️ 下一步
1. git add -A → 第一次 commit
2. 問使用者：要建 GitHub repo（公開）並啟用 Pages？→ push、確認 Actions 綠燈、開線上網址
3. （選用）Render 部署對戰後端 → 填 battle-api.js → 線上複驗對戰
4. 更新 Obsidian（L3）筆記

## ⚠️ 注意事項
- 絕對不要用 LibreOffice 轉中文 PDF（字型子集損壞）
- `questions.json`／`server.js`／`start-battle.bat` 不得上公開網站（pages.yml 已排除；questions.json 已進 .gitignore）
- 學生資料只用座號；不要把憑證寫進 repo
- index.html 內建 battle-api.js 與 #battleNote 切換邏輯，改版勿破壞

## 🕐 最後更新
- 時間：2026-11-10（本 session）
- 更新者：OpenCode（GLM）@ 本機
- Git push：待第一次 commit
