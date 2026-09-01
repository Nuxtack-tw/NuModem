# P3 HTTP / HTTPS 完整測試流程（可自行照做）

> 建立：2026-08-07｜對應程式版本：**V26.0.68**｜硬體：EG800K ＋ user 自製 CH343 控制板
> 本文所有「預期回應」都是 2026-08-07 實機跑出來的真實輸出，不是照手冊抄的。

## 緣起（user 提問）

> 你必須寫一個從連線到 modem 開機，啓動連線，取得 ip，到所有的 http 指令的測試流程寫一個詳細的報告，
> 這樣我才能自己測試一次
> —— 2026-08-07

---

## §1 這份文件怎麼用

- **每一步都有「操作」「預期回應」「判讀重點」三欄**，照順序做即可
- `☐` 是給你打勾的
- **「預期回應」欄裡的 `// 灰字` 是本工具自動加的註解**，不是模組送出來的。
  看不到註解的話，按終端機工具列的 💬 鈕打開
- 指令旁標注了**在哪個頁簽**。有按鈕的用按的；沒有的直接打進下方命令列
- ⏱ 標記代表該指令會阻塞較久，按下去要等，**不要連打**

⚠ **全程需要行動網路流量**（1NCE 預付卡）。整輪估算 §9，約 **15–25 KB**。

---

## §2 前置準備

| # | 項目 | 說明 | ☐ |
|---|---|---|---|
| 2-1 | 硬體接好 | CH343 控制板接 EG800K，USB 插上電腦 | ☐ |
| 2-2 | 天線接好 | 沒接天線 `AT+CSQ` 會很難看，HTTP 會一直逾時 | ☐ |
| 2-3 | 瀏覽器 | Chrome／Edge（Web Serial 只有 Chromium 系支援） | ☐ |
| 2-4 | 開啟程式 | `NuModem_EG800.html`，右上角版號應為 **V26.0.68** 以上 | ☐ |
| 2-5 | 序列埠沒被佔用 | **Web Serial 是獨佔的** —— 其他分頁或其他程式開著同一個埠就連不上 | ☐ |

---

## §3 步驟 A：連線與開機儀式

> ⚠ **這一步不能跳過。** 重新整理頁面會重開序列埠，重開埠會讓 RTS 重新 assert ——
> 而 **RTS 是模組電源（負邏輯，OFF＝通電）**，等於把模組斷電了。
> 所以「每次重新整理後都要重跑開機儀式」。

| # | 操作 | 預期回應 | 判讀重點 | ☐ |
|---|---|---|---|---|
| A-1 | 點右上「連線」，選 `CH343 [1A86:55D3]` | 終端出現 `已連接: CH343 @ 115200 bps`，按鈕轉綠 | 鮑率必須 **115200**、行尾必須 **CR** | ☐ |
| A-2 | **Hardware 頁** → 訊號列點 `RTS` 轉 **ON** | `RTS → ON` | ON＝**斷電**（負邏輯，別搞反） | ☐ |
| A-3 | 點 `DTR` 轉 **ON** | `DTR → ON` | DTR＝Reset 腳 | ☐ |
| A-4 | 點 `RTS` 轉 **OFF** | `RTS → OFF` | OFF＝**通電** | ☐ |
| A-5 | 點 `DTR` 轉 **OFF**，再轉 **ON** | `DTR → OFF`、`DTR → ON` | 放開 Reset | ☐ |
| A-6 | 等 8–30 秒 | `RDY`　`+CFUN: 1`　`+CPIN: READY`　`+QUSIM: 1`　`+QIND: SMS DONE`　`+QIND: PB DONE` | **看到 `RDY` 才算開機完成**；`PB DONE` 之後才算全部就緒 | ☐ |

**實測開機耗時**：7.8 秒 ～ 30.2 秒（兩次實測值都出現過，正常範圍）。

### A 步驟出問題時

| 症狀 | 原因與處置 |
|---|---|
| 選不到埠 | 其他分頁／程式佔著。關掉再試 |
| 一直沒有 `RDY` | RTS 邏輯搞反了（ON 是斷電）。重來一次，注意 A-2/A-4 |
| 有 `RDY` 但後面沒有 `+CPIN: READY` | SIM 沒插好或有 PIN 鎖，去 **Basic 頁**按 `AT+CPIN?` 確認 |

---

## §4 步驟 B：基本體檢（零流量）

| # | 操作 | 預期回應 | 判讀重點 | ☐ |
|---|---|---|---|---|
| B-1 | 命令列打 `AT` | `OK` | 沒有 `OK` 就是 AT 口沒通，回 §3 | ☐ |
| B-2 | **Basic 頁** → `ATE1 ⇄ ATE0` 確認是**開** | 之後每條指令都會被模組複誦一次 | 複誦讓終端可讀性大增，建議開著 | ☐ |
| B-3 | **Basic 頁** → `AT+CMEE=2` | `OK` | 錯誤碼變文字敘述。**要看數字碼請改 `AT+CMEE=1`** | ☐ |
| B-4 | **Hardware 頁** → `AT+QURCCFG="urcport"` | `+QURCCFG: "urcport","uart1"` | ⚠ **不是 `uart1` 就什麼 URC 都收不到**。按下面那顆 `…,"uart1"` 改掉 | ☐ |
| B-5 | **Network 頁** → `AT+CEREG?` | `+CEREG: 0,5`（漫遊）或 `0,1`（本網） | 1 或 5 都算已註冊 | ☐ |
| B-6 | **Network 頁** → `AT+CGATT?` | `+CGATT: 1` | 0 代表 PS 域沒附著，網路有問題 | ☐ |
| B-7 | **Network 頁** → `AT+CSQ` | `+CSQ: 24,99`（≈ -65 dBm，77%） | **低於 20% 就別測了**，HTTP 會一直逾時 | ☐ |
| B-8 | **TCP/IP 頁** → `AT+QGDCNT?` | 記下數字 | 流量基線，測完再看一次就知道用了多少 | ☐ |

---

## §5 步驟 C：取得 IP（PDP 啟用）

> 這一步有個**本卡專屬的坑**：SIM 只允許單一 PDP，而開機時網路會自動啟用一個，
> **編號會浮動**（實測見過 context 1、9）。`AT+QIACT=1` 撞到就會失敗。

| # | 操作 | 預期回應 | 判讀重點 | ☐ |
|---|---|---|---|---|
| C-1 | **Network 頁** → `AT+CGACT?` | `+CGACT: 1,1` 之類 | **記下「哪個 cid 是 1（已啟用）」** | ☐ |
| C-2 | **TCP/IP 頁** → `Act PDP`（`AT+QIACT=1`）⏱ 最長 150 秒 | `OK` | 別連打，等它回 | ☐ |
| C-3 | **TCP/IP 頁** → `Query IP`（`AT+QIACT?`） | `+QIACT: 1,1,1,"10.187.7.8"` | **有 IP 才算成功** | ☐ |
| C-4 | **TCP/IP 頁** → `AT+QPING=1,"8.8.8.8",4,4` ⏱ | `+QPING: 0,"8.8.8.8",32,155,114` ×4<br>`+QPING: 0,4,4,0,…` | **這一步不能省** —— 有 IP 不代表真的通 | ☐ |

### C 步驟失敗時：PDP 讓位

`AT+QIACT=1` 回 `ERROR`，按 `AT+QIGETERROR` 得到 `572 operation not allowed`：

```
AT+CGACT?              ← 看自動啟用的是哪個 cid（★ 編號會浮動，這步不能省）
AT+CGACT=0,<那個 cid>   ← 讓出名額     ⏱ 可能要等十幾秒
AT+QIACT=1             ← 再啟用一次   ⏱ 最長 150 秒
AT+QIACT?              ← 確認拿到 IP
```

### ⚠ 最重要的一個陷阱：`AT+QIACT?` 會騙人

實測遇過**測到一半 PDP 漂移**：所有 HTTP 請求突然全部失敗、
而且**固定 30 秒逾時**回 `716`，但 `AT+QIACT?` **照樣回 IP**，看起來一切正常。

真相要交叉比對才看得出來：

```
+QIACT: 1,1,1,"10.187.7.8"   ← Quectel 堆疊層說 context 1 有 IP
+CGACT: 1,0                   ← 3GPP 層說 context 1【未啟用】  ← 不一致！
+CGACT: 9,1                   ← PDP 已漂移到 context 9
```

**判準：連續 HTTP 失敗且逾時時間固定（30 秒）→ 先懷疑 PDP 漂移，不要怪伺服器。**

修法：

```
AT+QIDEACT=1
AT+CGACT=0,<漂移到的那個 cid>
AT+QIACT=1
AT+QPING=1,"8.8.8.8",4,2      ← 一定要 ping 過再繼續
```

---

## §6 步驟 D：HTTP 前置設定（零流量）

全部在 **HTTP 頁 → Config 群組**。

| # | 操作 | 值 | 為什麼 | ☐ |
|---|---|---|---|---|
| D-1 | `AT+QHTTPCFG="contextid"` 卡片 | PDP ID = `1` | 綁到剛啟用的 context | ☐ |
| D-2 | `AT+QHTTPCFG="rspout/auto"` 卡片 | 開關 = `0` | ⚠ **設 1 會讓 `QHTTPREAD` 一律失敗**（手冊明載） | ☐ |
| D-3 | `AT+QHTTPCFG="requestheader"` 卡片 | 開關 = `0` | ⚠ **`QHTTPGETEX` 只在此值為 0 時可執行** | ☐ |
| D-4 | `AT+QHTTPCFG="responseheader"` 卡片 | 開關 = `0` | 先關；3-9 才打開 | ☐ |
| D-5 | 按 `AT+QHTTPCFG?` | 一次讀回全部設定 | 對照上面四項是否生效 | ☐ |

---

## §7 步驟 E：十項測試

> 全部在 **HTTP 頁 → Transfer 群組**。
> `AT+QHTTPURL` 與 `AT+QHTTPPOST` 是**兩段式卡片**：只有一顆「送出（兩段式）」鈕，
> 長度欄位由程式自動算，你只要填 URL／內容。

### 3-1　設 URL（兩段式）

| | |
|---|---|
| **操作** | `AT+QHTTPURL` 卡片 → URL 欄填 `http://www.example.com/` → 按「送出（兩段式）」 |
| **預期** | `AT+QHTTPURL=23,80` → `CONNECT` → `http://www.example.com/　← payload 23 bytes，未加行尾` → `OK` |
| **接著** | 按 `AT+QHTTPURL?` → `+QHTTPURL: http://www.example.com/` |
| **判讀** | **長度必須是 23**。這串剛好 23 bytes，讀回一致就反證了「URL 沒有被附加 CR/LF」——<br>多一個字元就代表行尾跑進去了，後面所有測試都會歪 |
| ☐ | |

### 3-2　HTTP GET

| | |
|---|---|
| **操作** | `AT+QHTTPGET` 卡片 → 回應逾時 `80` → 送出 |
| **預期** | `OK` → `+QHTTPGET: 0,200`　`// GET 成功；HTTP 200 OK` |
| **判讀** | ⚠ **只有兩欄，沒有第三欄長度** —— `<content_length>` 是選填，一般 GET 不回。<br>**第一欄 0 是「指令成功」**，HTTP 狀態碼在第二欄 |
| ☐ | |

### 3-3　讀回應

| | |
|---|---|
| **操作** | `AT+QHTTPREAD` 卡片 → 等待逾時 `80` → 送出 |
| **預期** | `CONNECT` → 一整行 HTML（559 bytes，`<!doctype html>…</html>`）→ `OK` → `+QHTTPREAD: 0` |
| **判讀** | **`+QHTTPREAD: 0` 才是真正的結束標記，不是前面那個 `OK`**（註解會提醒）。<br>另外確認原始 HTML 沒有被誤判成某條指令的回應而亂標註解 |
| ☐ | |

### 3-4　分段取回（逐 byte 驗證）★

> 這項要換 URL，因為 `example.com` 驗不出「取對片段」——
> 必須用**內容固定且支援 HTTP Range** 的端點。

| | |
|---|---|
| **操作 1** | `AT+QHTTPURL` 卡片 → URL 改 `http://httpbin.org/range/16` → 送出（長度會自動變 27） |
| **操作 2** | `AT+QHTTPGETEX` 卡片 → 起始位移 `0`、取回長度 `8` → 送出 → 再按 `AT+QHTTPREAD` |
| **預期 2** | `+QHTTPGET: 0,206,8` → `CONNECT` → `abcdefgh` → `+QHTTPREAD: 0` |
| **操作 3** | `AT+QHTTPGETEX` → 起始位移 `8`、取回長度 `8` → 送出 → 再按 `AT+QHTTPREAD` |
| **預期 3** | `+QHTTPGET: 0,206,8` → `ijklmnop` |
| **判讀** | **狀態碼必須是 206 不是 200**。`abcdefgh` ＋ `ijklmnop` = `abcdefghijklmnop` 才算通過。<br>⚠ 若回 **200 且兩次內容一樣**，是**伺服器不支援 Range**（不是模組壞了）——<br>實測 `httpbin.org/base64/…` 就是這樣，所以一定要用 `/range/N` |
| ☐ | |

### 3-5　HTTP POST（兩段式）

| | |
|---|---|
| **操作 1** | URL 改 `http://httpbin.org/post` |
| **操作 2** | Config 群組 → `AT+QHTTPCFG="contenttype"` 卡片 → 型別碼 `0`（form-urlencoded） |
| **操作 3** | `AT+QHTTPPOST` 卡片 → POST內容欄填 `Message=HelloQuectel` → 按「送出（兩段式）」 |
| **預期** | `AT+QHTTPPOST=20,80,80` → `CONNECT` → payload 20 bytes → `OK` → `+QHTTPPOST: 0,200,440` |
| **接著** | 按 `AT+QHTTPREAD` → 一段 JSON |
| **判讀** | JSON 裡必須看到：<br>`"form": { "Message": "HelloQuectel" }` ← **證明 body 真的送達**<br>`"Content-Length": "20"` ← 長度算對<br>`"Content-Type": "application/x-www-form-urlencoded"` ← contenttype 生效<br>`"User-Agent": "QUECTEL_MODULE"` ← 模組自報的 UA |
| ☐ | |

### 3-6　HTTPS GET

| | |
|---|---|
| **操作 1** | **HTTP 頁 → Connect 群組**依序按：<br>`AT+QHTTPCFG="sslctxid",1`　`AT+QSSLCFG="sslversion",1,4`　`AT+QSSLCFG="ciphersuite",1,0XFFFF`　`AT+QSSLCFG="seclevel",1,0`　`AT+QSSLCFG="sni",1,1` |
| **操作 2** | URL 改 `https://www.example.com/`（注意是 **https**）→ 送出 |
| **操作 3** | `AT+QHTTPGET` → 送出 → 再 `AT+QHTTPREAD` |
| **預期** | `+QHTTPGET: 0,200` → HTML **與 3-3 逐字相同** |
| **判讀** | `seclevel 0` = 不驗憑證，這是本工具唯一走得完的路徑（要驗憑證得先把 CA 憑證寫進 UFS）。<br>body 與明文版一致，就證明 TLS 通道沒有把資料弄壞 |
| ☐ | |

### 3-7　異常路徑：DNS 失敗

| | |
|---|---|
| **操作** | 先 `AT+CMEE=1`（要看數字碼）→ URL 改 `http://no-such-host-numodem-test.invalid/` → GET |
| **預期** | `+CME ERROR: 716`　`// 裝置錯誤 716：HTTP socket 連線錯誤` |
| **判讀** | ⚠ **是 716 不是 714**。舊版計劃寫 714 是猜的，實測為 716。<br>接著按 `AT+QHTTPREAD` 會得到 `705`（沒有 GET/POST 請求）—— 這是正常的連鎖反應 |
| ☐ | |

### 3-8　異常路徑：HTTP 404

| | |
|---|---|
| **操作** | URL 改 `http://httpbin.org/status/404` → GET |
| **預期** | `+QHTTPGET: 0,404,0`　`// GET 成功；HTTP 404 Not found（找不到）；內容 0 bytes` |
| **判讀** | **第一欄的 `0` 是「指令執行成功」**，404 在第二欄。<br>很容易誤讀成失敗 —— 指令本身確實成功了，是伺服器說找不到 |
| ☐ | |

### 3-9　回應標頭

| | |
|---|---|
| **操作 1** | Config 群組 → `AT+QHTTPCFG="responseheader"` → 開關改 `1` |
| **操作 2** | URL 改 `http://httpbin.org/response-headers?X-Test=NuModem` → GET → READ |
| **預期** | `+QHTTPGET: 0,200,92`，讀回內容以 HTTP 標頭開頭：<br>`HTTP/1.1 200 OK` / `Content-Type: application/json` / `Content-Length: 92` / `X-Test: NuModem` |
| **判讀** | 有看到 `X-Test: NuModem` 就代表標頭區真的被帶出來了。**測完記得改回 `0`** |
| ☐ | |

### 3-10　轉址行為（手冊沒寫，本項就是要釐清）

| | |
|---|---|
| **操作 0** | ⚠ **先做對照組**：URL 設回 `http://www.example.com/` → GET，確認當下是 `0,200`。<br>沒有這步，下面的失敗分不清是轉址還是網路 |
| **操作 1** | URL 改 `http://httpbin.org/redirect/1`（Location 是相對路徑 `/get`）→ GET |
| **預期 1** | `+CME ERROR: 711`　`// HTTP URL 錯誤` —— **1 ms 立即失敗** |
| **操作 2** | URL 改 `http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F`（絕對）→ GET → READ |
| **預期 2** | `+QHTTPGET: 0,200`（152 ms）→ 讀回**是 example.com 的 HTML** |
| **判讀** | **結論：模組會自動跟隨 302，但只吃絕對 Location；相對路徑直接回 711。**<br>你的伺服器如果用相對轉址，模組就走不通 —— 這是實務上會踩到的限制 |
| ☐ | |

---

## §8 排障速查表

| 症狀 | 最可能的原因 | 處置 |
|---|---|---|
| `AT` 沒有 `OK`、ESC 也沒用 | 模組掛住（實測遇過兩次，手冊沒描述） | **重跑開機儀式**（§3） |
| 看不到任何 URC | `urcport` 不是 `uart1` | Hardware 頁改掉（B-4） |
| **所有 URL 都 716、固定 30 秒逾時** | **PDP 漂移**（`QIACT?` 會騙人） | `AT+CGACT?` 交叉比對 → §5 讓位流程 |
| `QHTTPREAD` 一律失敗 | `rspout/auto` 被設成 1 | 改回 `0`（D-2） |
| `QHTTPGETEX` 回 `ERROR` | `requestheader` 不是 0 | 改回 `0`（D-3） |
| `QHTTPGETEX` 回 200 且兩次內容相同 | **伺服器不支援 Range**，不是模組問題 | 換 `httpbin.org/range/N` |
| `+CME ERROR: 705` | 還沒送 GET/POST 就按 READ | 正常反應，先送請求 |
| `+CME ERROR: 704` | 別的埠佔著 data mode | 按 `AT+QHTTPSTOP` 收乾淨 |
| 換一條指令前狀態怪怪的 | 上一次請求沒收尾 | 按 `AT+QHTTPSTOP` |
| httpbin 突然全部失敗 | 社群服務限流 | 改用 `postman-echo.com` 對應端點 |

---

## §9 流量估算

| 階段 | 估算 |
|---|---|
| §4 基本體檢、§6 前置設定 | **0**（全部零流量指令） |
| C-4 ping ×4 | < 1 KB |
| 3-1～3-3（GET + 559 B body） | ≈ 1 KB |
| 3-4 分段 ×2 | < 1 KB |
| 3-5 POST + 440 B 回應 | ≈ 1 KB |
| **3-6 HTTPS（憑證鏈是大頭）** | **≈ 8–15 KB** |
| 3-7～3-10 | ≈ 2 KB |
| **合計** | **約 15–25 KB** |

測前測後各按一次 **TCP/IP 頁 → `AT+QGDCNT?`**，相減就是實際用量。

---

## §10 相關文件

- `reports/data-connection-test-plan.md` §P3 —— 測試計劃與逐項狀態（含 2026-08-07 實測結果）
- `reports/tcp-server-setup.md` §3 —— 各公開測試服務的實測數據
- `.claude/skills/EG800K_Modem_SKILL.md` §0-§2 —— 開機儀式與硬體時序的完整說明
- `changelog.md` V26.0.68 —— P3 過程中修掉的三個 bug
