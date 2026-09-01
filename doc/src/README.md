# 多語說明書建置原始碼

`doc/manual.html` 是**組裝產物**，來源在這個目錄。**不要直接改產出檔**，下次組裝就被蓋掉。

## 與母專案（NuMonitor4SerialPort）的差異

架構沿用母專案 `doc/src/` 那一套（head 共用、bodies 分語言、build.py 加前綴組裝），
但有三點不同，接手前先看清楚：

1. **zh-TW 是原始語言且必須內含。** 母專案的中文版另有獨立網站，所以它的
   `LANGS` 裡沒有 zh-TW；本專案相反 —— zh-TW 是所有翻譯的來源，也是文件端
   認不得語言時的退路。
2. **18 種語言，與主程式的語言清單完全一致。** 母專案只有 5 種。
3. **只有說明書，沒有 changelog.html。** 本專案的變更記錄是根目錄那份
   `changelog.md`（單一來源、只有繁中），主程式的徽章直接連過去，不參與這套組裝。

## 檔案

| 路徑 | 內容 |
|---|---|
| `build.py` | 組裝腳本；語言清單、選單名稱、頁面標題、額外 CSS 與切換邏輯都在裡面 |
| `check.py` | 結構驗證：拿每份譯文的 id／錨點／圖片／標籤數去比對 zh-TW 原文 |
| `manual.head.html` | 說明書的 `<head>`（含 CSS），18 種語言共用；`{LANG}` 與 `{TITLE}` 由 build.py 代入 |
| `bodies/manual.<lang>.html` | 各語言的正文，**要改內容就改這裡** |
| `../img/` | 12 張截圖，各語言共用（介面截圖目前都是繁體中文版） |

版本號**不在這裡維護** —— `build.py` 直接讀主程式 `NuModem_EG800.html` 的 `<title>`，
那是全專案版本號的唯一來源。

## 用法

```bash
python doc/src/check.py     # 先驗結構（會擋下最容易犯的翻譯錯誤）
python doc/src/build.py     # 組裝到 doc/manual.html
python doc/src/build.py <目錄>   # 產到別處（試作用）
```

## 改內容的流程

1. 改 `bodies/manual.zh-TW.html`（原始語言）
2. 把同樣的改動套到其餘 17 份 —— **HTML 結構必須逐字一致**，只換文字
3. `python doc/src/check.py` → 18/18 通過
4. `python doc/src/build.py`
5. 瀏覽器切過幾種語言看實際結果，RTL 語言要另外看

## check.py 擋的是什麼

翻譯 agent 最容易犯的錯不是翻錯字，是**順手改結構**：多一個標籤、把
`href="#faq"` 的錨點翻成當地語言、少一張圖。這類錯誤組裝出來不會報錯，
但導覽列會點不動、錨點會跳到隱藏的語言區塊。`check.py` 就是在組裝前攔下它們。

它比對五件事：`id` 清單、`href="#…"` 清單、`<img src>` 清單、各標籤的數量
（`<br>`／`<strong>`／`<em>`／`<code>` 容許斷句差異，其餘要完全相同）、
以及「每個錨點都指得到同一份正文裡的 id」。

## 加一種語言

1. 複製 `bodies/manual.zh-TW.html` → `bodies/manual.<語言碼>.html`，翻譯內容
2. `build.py` 的 `LANGS`、`LANG_NAMES`、`TITLES` 各補一條；由右至左書寫的語言要加進 `RTL`
3. `check.py` → `build.py`

**主程式不必動。** `LanguageManager.updateDocLinks()` 只負責把 `?lang=<介面語言>`
帶過去；要顯示哪一版、認不得時怎麼退回，全由文件端自己決定
（認不得的語言會退回繁體中文並在頁首顯示一條提示）。

## 已知缺口

- 12 張截圖都是**繁體中文介面**。其餘 17 種語言的正文是翻譯過的，但圖裡的介面仍是中文。
- 圖說（`<figcaption>`）有翻譯，所以看得懂在指什麼，只是圖本身沒有分語言版本。
