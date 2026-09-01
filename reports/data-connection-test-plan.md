# 數據連線實測計劃（SSL / HTTP / FTP / MQTT / TCP-IP / GNSS-AGPS）

> 建立：2026-08-05｜版本基線：V26.0.26｜狀態：**進行中**
> 進度勾稽：**逐項狀態記錄在本文件各表格的「狀態」欄**；`TODO.md` 只掛階段級勾選框。

## 緣起（user 提問）

> 我回來了，我現在配合你做需要連線的測試，你先寫一個測試計劃並列爲todo，因爲這個測試可能
> 要很多個工作天，中間也會修改很多程式。爲了確保我們不會漏掉測試計劃，才需要你做這個測試計劃
> —— 2026-08-05

背景：盤點報告（`at-command-coverage-audit.md`）四批已於 2026-08-02 完成，全部指令做過
**零流量語法驗證**（`=?` 逐條探測）。唯一未結案的就是「真實數據連線實測」——
SIM 是 1NCE 國際漫遊卡（MCC 901），先前一直等 user 裁決漫遊費。本計劃即該工作的完整拆解。

---

## §1 測試原則

1. **由小到大**：先 ping（KB 以下）再 HTTP，最貴的（HTTPS 憑證鏈、AGPS 下載）放後面。
2. **流量記帳**：每階段開始與結束都跑 `AT+QGDCNT?` 記入 §8 流量帳本。整份計劃核心項目
   預估 **< 40 KB**，含重試與選測抓 3 倍安全係數 **< 200 KB**（1NCE 終身 500 MB 的 0.04%）。
3. **驗收不只是指令成功**——每個測項有四個驗收面向：
   - a. 指令流程照手冊走完（含 URC 時序）
   - b. **終端每一行回應都有正確註解**（缺的當場補、錯的當場修 → 這就是「會改很多程式」的主體）
   - c. 兩段式指令（payload / CONNECT）的實作在真實網路下成立
   - d. 異常路徑的錯誤碼註解正確（拔線、逾時、伺服器拒絕）
4. **每次改程式照規矩走**：bump 版號 c、先 `cp` 快照到 `backup/`、記 `changelog.md`。
   同一天多輪小修可以併成一個版號條目，但**測試中發現的 bug 修正不可與功能擴充混在同一條**。
5. **可中斷、可續測**：每階段獨立，中斷後從任一階段重來。開機儀式後 PDP context 1 會自動啟用
   （實測 IP 10.187.7.8），不需要重做前面的階段。

## §2 每次開測的前置儀式（P0，零流量）

每個工作天開始、或模組斷電重啟後，依序執行（細節見技能檔 §2）：

| # | 動作 | 預期 | 狀態 |
|---|---|---|---|
| 0-1 | 開機儀式（RTS ON→OFF、DTR ON→OFF→ON） | `RDY` → `+QIND: SMS DONE` / `PB DONE` | ☐ |
| 0-2 | `ATE1`＋`AT+CMEE=2` | 複誦開、錯誤碼文字化 | ☐ |
| 0-3 | `AT+CPIN?` → `AT+CEREG?` → `AT+QIACT?` | READY／已註冊（漫遊 5 正常）／context 1 有 IP | ☐ |
| 0-4 | `AT+QURCCFG="urcport"` | **必須是 `uart1`**，否則所有結果 URC 都看不到 | ☐ |
| 0-5 | `AT+QGDCNT?` 記入流量帳本 | 基線數字 | ☐ |
| 0-6 | `AT+CSQ` 記訊號 | 太差（< 20%）當天測試結果要打折看待 | ☐ |

## §3 測試階段

### P1 TCP/IP 診斷三件套（預估 4 KB）

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 1-0 | **前置：讓出 PDP 名額**（見下方排障） | `AT+CGACT?` → `AT+CGACT=0,<該 cid>` → `AT+QIACT=1`（**QICSGP 可省**） | `+QIACT: 1,1,1,"10.187.7.8"` | ✔ |
| 1-1 | Ping IP（避開 DNS 變因） | `AT+QPING=1,"8.8.8.8",4,4` | ✔ 4 球全通、RTT 160-270 ms、0 掉包 | ✔ |
| 1-2 | Ping 域名 | `AT+QPING=1,"www.example.com",4,4` | ✔ 解析為 104.20.23.154、RTT 160-175 ms | ✔ |
| 1-3 | DNS 解析 | `AT+QIDNSGIP=1,"www.google.com"`（2026-08-06 user 指定改用 google） | ✔ 兩段 URC + 多筆 IP | ✔ |
| 1-4 | NTP 對時 | `AT+QNTP=1,"pool.ntp.org",123` | ✔ `+QNTP: 0,"2026/08/06,12:40:04+32"`；`QLTS` 20:40:23（見下方 UTC 陷阱） | ✔ |

**註解已於 V26.0.52 補完**（`+QPING` 逐球與統計兩式、`+QIURC: "dnsgip"` 兩段、`+QNTP`、
`+QIACT?`，另補 `+QIURC: recv/closed/pdpdeact` 與 `SEND OK/FAIL`），真機實測全部正確顯示。

### 🔴 P1 排障：本卡只允許單一 PDP，且自動啟用的 context 編號浮動

**症狀**：`AT+QIACT=1` 回 `ERROR`，`AT+QIGETERROR` → `572,operation not allowed`。

**追查**：
1. 開機後 3GPP 層已自動啟用一個 PDP 並取得 IP，但**編號會變**（實測見過 context 9 與 context 1）
2. `AT+CGACT=1,1`（3GPP 層再開一個）→ `+CME ERROR: 100` ⇒ **網路只允許單一 PDP**
3. `AT+QIACT` 的 contextID 範圍是 **(1-8)** —— 若網路把 PDP 開在 context 9，Quectel 堆疊層**根本碰不到**

**解法（P1 起每次開機都要做，共兩步）**：

```
AT+CGACT?            → 看自動啟用的是哪個 cid（★ 編號會浮動，這步不能省）
AT+CGACT=0,<那個 cid>  → 讓出名額
AT+QIACT=1           → +QIACT: 1,1,1,"10.187.7.8"
```

**`AT+QICSGP` 不需要**（2026-08-06 user 指出並實測驗證）：開機當下讀 `AT+QICSGP=1`
就已經是 `iot.1nce.net` —— 模組會從網路配下來的 PDP 定義自動同步 APN
（`AT+CGDCONT?` 三個 context 的 APN 全是它）。手冊說「須先 QICSGP 設好參數」是通則，
本卡的前提本來就成立。**換成 APN 不會自動配下來的卡（例如需帳密的企業 APN）時仍然必要。**

此後 P2-P6 全部沿用 context 1。

### ⚠ `+QNTP` 的時間是 UTC，卻帶本地時區標記

實測 `+QNTP: 0,"2026/08/06,12:40:04+32"`，同時 `AT+CCLK?` 回 `20:40:17`、
`AT+QLTS=2` 回 `20:40:23` —— **差正好 8 小時**。`+32` 是時區標記（32 刻＝GMT+8），
但時間欄位本身是 UTC。要看本地時間請用 `AT+CCLK?`。註解已寫明此陷阱。

### P2 TCP socket 收發（預估 3 KB）

**echo 伺服器：`tcpbin.com:4242`（免費公開，零設定）** —— 已是程式 V26.0.58 的內建預設值，
`AT+QIOPEN` 一按即用。原本規劃自架，但 user 提出產品層級約束
（「numodem 是要給各種消費者使用，他們不一定能修改 router 的設定」）後改為公開服務優先：
模組是 TCP client，只需要「一台從外網連得到的伺服器」，不需要使用者家裡開埠。
echo 的往返比對同樣能逐 byte 驗證資料正確性，自架的優勢只剩「製造異常情境」。

**2-8／2-9 仍需自架**（`tools/tcp_test_server.py`，可行性排序見 `reports/tcp-server-setup.md` §4）——
公開 echo 無法主動斷線、也無法在連上時主動推資料。
自架時讓模組連得到的首選是**通道服務**（`bore local 5000 --to bore.pub`，不必碰路由器、不必註冊）；
本機雖有真公網 IP `36.239.107.43`（非 CGNAT）可走連接埠轉發，但**路由器實測沒開
UPnP／NAT-PMP／PCP**（`tools/nat_probe.py` 三協定全滅），無法自動開埠。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 2-1 | 開 TCP 連線（buffer 模式） | `AT+QIOPEN=1,0,"TCP","<公網IP>",5000,0,0` | `OK` → `+QIOPEN: 0,0`；伺服器畫面出現「連線建立」 | ☐ |
| 2-2 | 連線狀態 | `AT+QISTATE` | 欄位解讀正確（state 2 connected） | ☐ |
| 2-3 | 送 hex 資料 | `AT+QISENDEX=0,"48656C6C6F0A"`（"Hello\n"） | `SEND OK` → echo 觸發 `+QIURC: "recv",0` | ☐ |
| 2-4 | 讀回 echo | `AT+QIRD=0,1500`，再讀一次到 `+QIRD: 0` | 讀出 6 bytes，內容 = Hello | ☐ |
| 2-5 | 查緩衝 | `AT+QIRD=0,0` | 三數字（總收/已讀/未讀）解讀正確 | ☐ |
| 2-6 | 關閉 | `AT+QICLOSE=0` | `OK`；再 `AT+QISTATE` 應為空 | ☐ |
| 2-7 | 異常路徑 | 對已關閉的 socket 送 `AT+QISENDEX` | 錯誤碼註解正確 | ☐ |
| 2-8 | **對端主動斷線** | 連上後**閒置 15 秒**（tcpbin 逾時，不必自架） | 模組收到 `+QIURC: "closed",0`，`AT+QISTATE` 的 state 變 4（closing） | ☐ |
| 2-8b | 重用 connectID | 收到 closed 後直接 `AT+QIOPEN`（不先 QICLOSE） | 應回錯誤 **563**；`AT+QICLOSE=0` 後才能重開 | ☐ |
| 2-9 | **被動接收**（自架才測得到） | 伺服器加 `--send-on-connect "hi\n"` | 連上即收到 `+QIURC: "recv",0`，`AT+QIRD` 讀得出內容 | ☐ |

### P2 的三個實測陷阱（2026-08-07，user 逐一撞到）

1. **2-3 結尾的 `0A` 不可省** —— tcpbin.com 是**以行為單位**的 echo 伺服器，
   沒收到換行就一直緩衝著不回送：送 `Hello`（無 0A）等 6 秒毫無回應，補一個 0A 後 0.1 秒立刻收到。
   V26.0.58 換對端時預設 hex 還是舊的 `48656C6C6F`，**V26.0.61 已修**。

2. **2-4 要讀到 `+QIRD: 0` 為止** —— 沒讀乾淨，模組不會再發下一次 `recv` 通知，下一筆就等不到
   （手冊 §2.3.9／§2.4.2 明載此抑制行為）。
   若 `AT+QIRD` 手動下去有資料、卻收不到 `+QIURC: "recv"`，那是 URC 沒進 UART ——
   去 Hardware 頁查 `AT+QURCCFG="urcport"` 是不是 `uart1`（本專案已踩過三次）。

3. **`+QIURC: "closed",0` 不是 `AT+QIRD` 造成的** —— tcpbin.com 有 **15 秒閒置逾時**
   （實測：送完一行後 15.1 秒收到 FIN；連上完全不送也是 15.1 秒；每 3 秒送一行則不會斷）。
   手動點按鈕很容易超過 15 秒，所以 closed 常在按下 Read Data 前後冒出來，看起來像因果關係。
   **`AT+QIRD` 只讀模組本地緩衝，不與伺服器通訊**；手冊 §2.4.1 寫明 `closed` 僅在
   「遠端關閉或網路錯誤」時發出。要維持連線就每 10 秒內送一次資料。
   —— 這個逾時反而讓 **2-8 不必自架伺服器就測得到**（原規劃要 `--drop-after`）。

**已知註解缺口**：`+QIOPEN: <id>,<err>`、`+QIURC: "recv"/"closed"/"pdpdeact"`、
`SEND OK`／`SEND FAIL`、`+QIRD:` 各型、`+QISTATE:` 欄位解讀。

### P3 HTTP / HTTPS（預估 20 KB，HTTPS 憑證鏈是大頭）

**測試對端（2026-08-07 實測選定）**

| 用途 | 位址 | 實測 | 為什麼選它 |
|---|---|---|---|
| **基本 GET** | `http://www.example.com/` | 200，**559 bytes**，470 ms | body 小、二十年不變；URL 剛好 **23 bytes**，與手冊 §3.1.1 的 `AT+QHTTPURL=23,80` 範例對得起來 |
| **HTTPS GET** | `https://www.example.com/` | 200，559 bytes，643 ms | 同站同內容，可與明文結果逐 byte 對照 |
| **逐 byte 驗證** ★ | `http://httpbin.org/bytes/16` | 200，**剛好 16 bytes** | 長度可指定，`QHTTPGETEX` 的 offset／length 才驗得準 |
| **POST echo** | `http://httpbin.org/post` | 200，445 bytes | 回吐 body，能證明模組真的送出去了什麼 |
| **請求標頭 echo** | `http://httpbin.org/headers` | 200，183 bytes | 驗 `QHTTPCFG="reqheader/add"` 有沒有生效 |
| **回應標頭** | `http://httpbin.org/response-headers?X-Test=NuModem` | 200，92 bytes | 驗 `QHTTPCFG="responseheader",1` |
| **狀態碼路徑** | `http://httpbin.org/status/404` | 404 | 非 2xx 的註解判讀 |
| **轉址行為** | `http://httpbin.org/redirect/1` | **302 → /get** | 模組會不會自動跟隨（手冊未明說，實測釐清） |
| 備援 | `postman-echo.com/get`／`/post`／`/status/404` | 168／313／404 | httpbin 是社群維運、偶有限流；Postman 是商業服務較穩 |

⚠ **`neverssl.com` 不能用** —— 2026-08-06 實測回 403，2026-08-07 再測直接連不上。

**選擇理由**：`httpbin.org` 是唯一同時提供「**指定長度**、**POST 回吐**、**標頭回吐**、**狀態碼**」四種端點的免費服務，
而這四種正好對應 P3 要驗的四條路徑。缺點是社群維運、偶有限流，所以並列 `postman-echo.com` 當備援。
`example.com` 則是最穩的基準點（body 559 bytes，不怕洗版也不吃流量）。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 3-1 | 設 URL（兩段式 CONNECT） | `AT+QHTTPURL=23,80` → `http://www.example.com/` | ✔ `CONNECT` → 23 bytes → `OK`；`AT+QHTTPURL?` 讀回完全一致（**反證未附加行尾字元**） | ✔ |
| 3-2 | HTTP GET | `AT+QHTTPGET=80` | ✔ `+QHTTPGET: 0,200` —— ⚠ **只有兩欄，沒有 content_length**（手冊標為選填），與原計劃預期的三欄不同 | ✔ |
| 3-3 | 讀回應 | `AT+QHTTPREAD=80` | ✔ `CONNECT` → 559 bytes HTML → `OK` → `+QHTTPREAD: 0`；**原始 HTML 未誤觸其他註解規則** | ✔ |
| 3-4 | 部分取回（逐 byte） | `http://httpbin.org/range/16`，`GETEX=80,0,8` 與 `=80,8,8` | ✔ 兩次皆 `+QHTTPGET: 0,206,8`；`abcdefgh` ＋ `ijklmnop` = `abcdefghijklmnop` **逐 byte 相符** | ✔ |
| 3-5 | HTTP POST（兩段式） | `AT+QHTTPPOST=20,80,80` → `httpbin.org/post`，body `Message=HelloQuectel` | ✔ `+QHTTPPOST: 0,200,440`；回吐 `"form": {"Message": "HelloQuectel"}`、`Content-Length: 20`、`User-Agent: QUECTEL_MODULE` | ✔ |
| 3-6 | HTTPS GET | `sslctxid 1`＋`sslversion 4`＋`seclevel 0`＋`sni 1` → `https://www.example.com/` | ✔ TLS 交握成功、`+QHTTPGET: 0,200`、body 與 3-2 逐字相同 | ✔ |
| 3-7 | 異常路徑（DNS） | GET `http://no-such-host-numodem-test.invalid/` | ✔ `+CME ERROR: 716`（HTTP socket 連線錯誤）—— ⚠ **不是原計劃預期的 714** | ✔ |
| 3-8 | 異常路徑（狀態碼） | `http://httpbin.org/status/404` | ✔ `+QHTTPGET: 0,404,0` —— **第一欄 0 是「指令成功」**，404 在第二欄 | ✔ |
| 3-9 | 回應標頭 | `responseheader,1` → `httpbin.org/response-headers?X-Test=NuModem` | ✔ `0,200,92`；讀回含完整 HTTP 標頭區與 `X-Test: NuModem` | ✔ |
| 3-10 | 轉址行為 | `httpbin.org/redirect/1`（相對）vs `redirect-to?url=…`（絕對） | ✔ **模組會自動跟隨 302，但只吃絕對 Location**：絕對 → `0,200` ＋ 目標站 body（152 ms）；相對 `/get` → **711 URL 錯誤**（1 ms） | ✔ |

**P3 全數通過（2026-08-07 實機，Playwright 驅動）。**

### P3 查出的事實（手冊未寫或與計劃預期不符）

1. **`+QHTTPGET` 的 `<content_length>` 是選填** —— 一般 GET 只回 `0,200` 兩欄；
   `GETEX`／`POST`／404 那幾次才有第三欄。判讀時不能假設一定有三欄。
2. **DNS 失敗回 716 不是 714** —— 原計劃寫 714 是猜的，實測為 `716 HTTP socket 連線錯誤`。
3. **轉址只支援絕對 Location** —— 手冊完全沒提。相對路徑 `/get` 立即回 711。
   ⚠ 這條結論**做過對照組**：先確認 `example.com` 當下 200 正常，才比較兩種轉址。
4. **`QHTTPGETEX` 依賴伺服器支援 HTTP Range** —— 手冊說「always respond with 206」，
   但那是**伺服器有支援**的前提下。實測 `httpbin.org/base64/…` 不支援 Range，
   兩次不同位移都回 200 加整份內容，看起來像模組沒生效。要用 `httpbin.org/range/N` 才驗得準。
   另：手冊明載此指令**只在 `QHTTPCFG="requestheader",0` 時可執行**。

### ⚠ P3 過程中發生的網路故障（重要排障案例）

測到一半所有 URL 全部 `716` 且**固定 30 秒逾時**，連 15 分鐘前還正常的 `example.com` 也一樣。
對照組證實不是轉址造成的。診斷後發現**兩層 PDP 狀態不一致**：

```
+QIACT: 1,1,1,"10.187.7.8"   ← Quectel 堆疊層說 context 1 有 IP
+CGACT: 1,0                   ← 3GPP 層說 context 1 【未啟用】
+CGACT: 9,1                   ← PDP 已漂移到 context 9
+QPING: 559 / 550             ← socket 讀取失敗
```

**`AT+QIACT?` 這時候會騙人** —— 它照樣回 IP，看起來一切正常。
必須與 `AT+CGACT?` 交叉比對才看得出漂移。

解法（與 P1 同一招，但這次是**測到一半才漂移**，不是開機時）：

```
AT+QIDEACT=1
AT+CGACT=0,<漂移到的那個 cid>
AT+QIACT=1
AT+QPING=1,"8.8.8.8",4,2     ← 驗證真的通了再繼續
```

**教訓：長時間測試中途要定期用 `AT+CGACT?` 交叉檢查，不能只信 `AT+QIACT?`。**
連續 HTTP 請求失敗且逾時時間固定，優先懷疑 PDP 漂移而不是伺服器。

### P4 MQTT（預估 5 KB）

broker：`test.mosquitto.org:1883`（備援 `broker.hivemq.com` / `broker.emqx.io`，皆免認證）。
clientid 與 topic 帶隨機尾碼避撞：`numodem-<4碼>`、`numodem/test/<4碼>`。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 4-1 | 設定 | `AT+QMTCFG="version",0,4`＋keepalive | OK | ☐ |
| 4-2 | 開網路連線 | `AT+QMTOPEN=0,...` | `OK` → `+QMTOPEN: 0,0` | ☐ |
| 4-3 | MQTT CONNECT | `AT+QMTCONN=0,"numodem-xxxx"` | `+QMTCONN: 0,0,0` | ☐ |
| 4-4 | 訂閱 | `AT+QMTSUB=0,1,"numodem/test/xxxx",0` | `+QMTSUB: 0,1,0,0` | ☐ |
| 4-5 | **兩段式發布（核心驗收）** | `AT+QMTPUBEX` 發到同一 topic | `>` 流程走通 → `+QMTPUBEX: 0,x,0` → **收到自己的 `+QMTRECV`（自迴路）** | ☐ |
| 4-6 | 中文 payload | payload 帶中文（UTF-8 長度自動算） | `+QMTRECV` 內容不截斷不亂碼 | ☐ |
| 4-7 | 退訂＋斷線 | `AT+QMTUNS` → `AT+QMTDISC` | `+QMTUNS`／`+QMTDISC: 0,0` | ☐ |
| 4-8 | 異常路徑 | 對不存在的 broker `QMTOPEN` | 錯誤碼註解正確 | ☐ |

4-5 是 V26.0.22 `sendWithPayload()` 實作的**終極驗收**——自迴路收到的訊息位元組數
必須等於送出時自動計算的長度。

**已知註解缺口**：`+QMTOPEN/+QMTCONN/+QMTSUB/+QMTUNS/+QMTPUBEX/+QMTDISC` 結果 URC、
`+QMTRECV`（訊息內容）、`+QMTSTAT`（異常斷線）。MQTT 結果全是「先 OK 再 URC」模式，同 FTP。

### P5 SSL raw socket（預估 12 KB）

TLS echo 伺服器：**`tcpbin.com:4243`**（2026-08-06 實測可連）。
選 echo 而非 `example.com:443` 的理由：443 只驗得到交握，**echo 才能逐 byte 驗證資料真的穿過 TLS 通道**。
⚠ 程式的 `AT+QSSLOPEN` 預設值目前**仍是 `example.com:443`** —— 本階段開跑時再一併改，手動填入亦可。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 5-1 | SSL 參數 | sslversion 4／ciphersuite 0XFFFF／seclevel 0 | OK；查詢式讀回一致 |✅ |
| 5-2 | 開 TLS 連線（buffer） | `AT+QSSLOPEN=1,1,4,"tcpbin.com",4243,0` | `+QSSLOPEN: 4,0` 註解「交握完成」 |✅ |
| 5-3 | 狀態 | `AT+QSSLSTATE` | 11 欄解讀正確（V26.0.26 tokenizer） |✅ |
| 5-4 | 兩段式送資料 | `AT+QSSLSEND=4,<len>` | `>` 流程；echo 觸發 `+QSSLURC: "recv",4` |✅ |
| 5-5 | 讀回 | `AT+QSSLRECV=4,1500` | `+QSSLRECV: <n>` + 資料；讀到 `0` 為止 |✅ |
| 5-6 | 關閉 | `AT+QSSLCLOSE=4` | OK；狀態回 initial |✅ |
| 5-7 | direct push 模式 | `AT+QSSLOPEN=...,1` 短測一輪 | `+QSSLURC: "recv",4,<len>` + 資料直出 |✅ |
| 5-8 | 異常路徑 | seclevel 1（無憑證）連線 | 交握失敗，錯誤碼註解正確（預期 SSL 5xx） |✅ |
| 5-9 | **憑證驗證真的有在動**（seclevel 1／2） | 連 `expired.badssl.com:443`、`self-signed.badssl.com:443`、`wrong.host.badssl.com:443`、`untrusted-root.badssl.com:443` | **四個都必須連不上**且錯誤碼各自合理。連得上＝驗證沒生效，此測項不通過 |✅ |
| 5-10 | 正對照組 | 同上設定連 `badssl.com:443` | **必須成功** —— 否則 5-9 的失敗只是「全部都連不上」，證明不了驗證有效 |✅ |

註解已於 V26.0.26 備妥，本階段驗實戰。
5-9／5-10 必須成對執行：**只有「壞憑證失敗＋好憑證成功」同時成立，才證明憑證驗證真的生效。**

**2026-08-07 實測完成，10/10 通過** —— 完整記錄見 `reports/p5-ssl-test-results.md`。三個要點：

- 憑證**送得進去**：PEM 是純 ASCII，`AT+QFUPL` + `writeRaw()` 已成功上傳 1939 bytes 的 ISRG Root X1。
  程式裡原本那句「本工具送不出二進位檔所以 seclevel 1/2 必定失敗」是錯的，已更正
- **`sni` 出廠預設 0，不開就驗不過** —— badssl.com 同 IP 掛多網域，不送 SNI 會拿到不匹配的憑證（566）。
  一度誤判成模組時鐘問題，查 `AT+CCLK?` 才排除
- ⚠ **連續開關 SSL 連線約 20 次後整個資料堆疊會退化**（連純 `AT+QIOPEN` 都回 552），
  `QIDEACT`+`QIACT` 救不回來，只有開機儀式能復原。此現象污染過中間資料，
  上表是重開機後的乾淨數據

### P6 FTP（預估 6 KB）

伺服器：`ftp.dlptest.com`（**可寫**，公開帳密見 https://dlptest.com/ftp-test/ ——
會不定期更換，開測當天先上網頁抄最新的；檔案約 30 分鐘自動刪）。
備援：`test.rebex.net`（`demo`/`password`，**唯讀**，只能測瀏覽與下載）。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 6-1 | 帳密＋被動模式 | `AT+QFTPCFG="account"...`＋`"transmode",1` | OK |✅ |
| 6-2 | 登入 | `AT+QFTPOPEN="ftp.dlptest.com",21` | `+QFTPOPEN: 0,0` 註解「登入成功」 |✅ |
| 6-3 | 目錄操作 | `QFTPPWD` → `QFTPCWD` → `QFTPLIST ,"COM:"` | data mode 清單顯示；`+QFTPLIST: 0,<n>` |✅ |
| 6-4 | **兩段式上傳（核心驗收）** | `AT+QFTPPUT="numodem-test.txt","COM:",0,<len>,1` | CONNECT → 送 payload → `+QFTPPUT: 0,<len>` 長度一致 |✅ |
| 6-5 | 檔案屬性 | `QFTPSIZE`＋`QFTPMDTM` 對上傳的檔 | 大小 = payload 長度 |✅ |
| 6-6 | 下載回來比對 | `AT+QFTPGET="numodem-test.txt","COM:"` | data mode 內容與上傳一致 |✅ |
| 6-7 | 改名＋刪除 | `QFTPRENAME` → `QFTPDEL` | `0,0`；再 SIZE 應回 550 類錯誤且註解正確 |✅ |
| 6-8 | 登出 | `AT+QFTPCLOSE` | `+QFTPCLOSE: 0,0` |✅ |
| 6-9 | data mode 逃逸（謹慎，最後做） | `QFTPGET COM:` 傳輸中按 `+++` → `ATO` 恢復 | 逃逸成功、ATO 續傳；模組不卡死 |⚠ |
| 6-10 | （選測）FTPS explicit | rebex＋`"ssltype",1`＋sslctxid | TLS 控制通道登入成功 |⏸ |

註解已於 V26.0.26 備妥（`+QFTPxxx` 統一解讀器 + `FTP_PROTO_ERRORS`）。

**2026-08-07 實測：8 通過 / 1 部分 / 1 選測未做**（6-7 於同日稍晚補做完成） —— 完整記錄見 `reports/p6-ftp-test-results.md`。三個要點：

- ⚠ **`AT+QFTPCLOSE` 是非同步的**：`OK` 只代表指令收下，必須等 `+QFTPCLOSE: 0,0`；
  期間狀態是 3（關閉中），這時下任何 FTP 指令一律 `+CME ERROR: 603`。
  這個坑會偽裝成「模組壞了」，本輪為此繞了很久
- ⚠ **`+++` 是中止不是暫停**：逃逸後狀態回到 1（閒置）、`ATO` 回 `NO CARRIER`，
  **與手冊 p13 寫的「ATO 可重入資料模式」不符**（兩次不同時機的測試結果一致）
- **dlptest 的被動資料連線不可靠**（`+CME ERROR: 615`），行動網路與家用寬頻兩條路徑症狀一致，
  是伺服器端問題。**讀取類測試改以 `test.rebex.net` 為主**，寫入類才用 dlptest 且要一氣呵成

6-4 的驗證刻意不靠模組自己：從主機端用 `ftplib` 把檔案讀回來比對，逐 byte 相符。

### P7 定位加速與網路定位（選測，做前再確認流量）

**兩種不同技術併在此階段測**（都要 PDP＋流量，且都是「定位」主題）：
AGNSS＝用網路輔助資料加速 **GNSS** 定位；QLBS＝完全不靠衛星，用 **Wi-Fi／基地台**
查雲端資料庫定位（室內可用）。

**前置**：`AT+QIACT=1` 已啟用（P1 做過）、GNSS 相關測試建議在窗邊/戶外。

#### P7-A AGNSS（GNSS 加速，V26.0.46 已備按鈕於 GNSS 頁「Accel」羣）

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 7-1 | 現況記錄 | `AT+QGPSCFG="apflash"`／`AT+QAGPS?`／`AT+QAGPSCFG?` | 實測出廠：apflash=1、AGNSS=0、伺服器 asrmicro allstar |✅ |
| 7-2 | **冷啟動基準時間** | 斷電重開 → `AT+QGPS=1` → 輪詢 `AT+QGPSLOC=2` 到成功 | 記錄 TTFF（對照組；user 實測曾 >10 分鐘） |⛔ |
| 7-3 | 啟用 AGNSS | `AT+QAGPS=1` → **重開機**（本指令重開機才生效） | `AT+QAGPS?` 回 1 |⛔ |
| 7-4 | AGNSS 下載與定位 | `AT+QGPS=1` → 看 `+QGPS: "agps",0,<code>` URC | code 0=成功／5=撥號錯誤／6=socket 錯誤（註解已備）；**TTFF 與 7-2 對比**；記流量 |⛔ |
| 7-5 | NMEA 讀取 | `AT+QGPSGNMEA="GSV"/"GGA"` | 語句解析正常、衛星圖同步更新 |◐ |

#### P7-B QLBS／QuecLocator（Wi-Fi＋基地台網路定位，2026-08-06 user 指定納入）

**本機韌體支援已確認**（`AT+QLBSCFG=?` 回七子項）；`AT+QLBS` 是執行式指令。

**2026-08-07 實測：3 完成 / 2 無法測 / 4 卡 token** —— 完整記錄見 `reports/p7-location-test-results.md`。

- **7-11 已完成**：Wi-Fi Scan 頁已備妥 QLBS 按鈕群與註解，**token 一到手就能直接開測**
- ⚠ **QLBS 在本專案的 16 份 PDF 裡一個字都沒有** —— QuecLocator 另有專屬應用文件，
  取得後應補進 `../_ref/EG800K/`。目前所有說明只寫實測事實，推測的部分都有標示
- **沒 token 與假 token 都回 `+QLBS: 702`**；token 讀回時被模組遮成 `*`
- ⚠ **設定用小寫鍵、讀回卻是駝峰**（`latorder` → `latOrder`）
- 7-2～7-4 因 user 所在位置室內完全無衛星訊號（`$GNGGA` 使用衛星 00 顆）而無法測；
  **7-2 是 7-4 的對照組，沒有天空視野時兩者都定不出來，測了只會得到「兩邊都失敗」**
**卡關前提：需要 Quectel 核發的 token**，本機未設 —— 沒 token 這段只能做到 7-6 為止。

| # | 測項 | 指令 / 目標 | 驗收 | 狀態 |
|---|---|---|---|---|
| 7-6 | 組態現況（零流量，可先做） | `AT+QLBSCFG=?`／逐一查 `"server"`／`"token"`／`"timeout"`／`"latorder"` 等 | 記錄出廠值；確認 token 是否為空 |✅ |
| 7-7 | **取得並設定 token** | `AT+QLBSCFG="token","<token>"`（token 需向 Quectel 申請） | 設定成功、查詢讀得回 |⛔ |
| 7-8 | 定位查詢 | `AT+QLBS`（執行式；先確認 PDP 已啟用） | 回座標＋精度；**與 GNSS 定位結果比對誤差**（預期數十公尺級） |⛔ |
| 7-9 | 熱點數量對定位的影響 | 先 `AT+QWIFISCAN` 調高 maxbssid（**本機上限 10**）再 QLBS | 熱點多寡與精度關係記錄 |⛔ |
| 7-10 | 室內可用性驗證 | 在 GNSS 定不出來的室內位置跑 QLBS | **這是 QLBS 的核心價值** —— 室內能定出位置即成功 |⛔ |
| 7-11 | 按鈕與註解 | 做前先 `=?` 探測語法 → WiFiScan 頁加 QLBS 羣＋回應註解 | 按鈕齊、每行有註解 |✅ |

### P8 收尾（零流量）

| # | 動作 | 狀態 |
|---|---|---|
| 8-1 | `AT+QGDCNT?` 總帳，填完 §8 | ✅ 2026-08-08 —— **但沒有總帳可拿**，原因見 §8 |
| 8-2 | 技能檔 §4 補所有新實測記錄、§5 勾掉「數據功能實測」 | ✅ 2026-08-08 |
| 8-3 | `TODO.md`／`changelog.md`／盤點報告 §7／`MEMORY.md` 收尾 | ✅ 2026-08-08 |

## §4 已知的程式修改預期（測試中會做的工作）

- **註解缺口**（P1/P2/P4 各表已列）：`+QPING`、`+QIURC` 家族、`+QNTP`、`+QIDNSGIP`、
  `SEND OK/FAIL`、`+QIRD`、`+QISTATE`、`+QMT*` 全家族。建議**每階段開測前先補齊該階段的註解**，
  邊測邊驗，而不是測完回頭補。
- **QLBS 按鈕與註解**（P7-11）：WiFiScan 頁加 QLBS 羣（`AT+QLBS` 執行式＋`AT+QLBSCFG` 子項），
  照慣例先 `=?` 零流量探測再上；回應格式要等實測才知道（手冊未在既有抽取範圍內）。
- ~~GNSS 頁簽補 XTRA 按鈕~~ → **已由 V26.0.46 的 Accel 羣取代**（apflash／QAGPS／QAGPSCFG；
  另實測 `AT+QGPSVBCKP` 本機韌體不支援）。
- data mode 顯示行為可能要調（HTML/清單原始輸出會不會誤觸註解、會不會排版亂掉）——實測才知道。
- 測試中發現的任何 bug 照 §1-4 規矩入版。

## §5 風險與脫困程序

| 狀況 | 症狀 | 脫困 |
|---|---|---|
| data mode 卡死 | payload 長度算錯，送什麼都被當資料吞掉 | 等 input timeout（本工具都設 80s）→ `+++` 鈕 → 最後手段 Hardware 頁 Reset |
| PDP 卡死 | QIACT 逾時、所有連線指令失敗 | `AT+QIDEACT=1`（最長 40s）→ 重新 `AT+QIACT=1` → 不行就 `AT+CFUN=1,1` 軟重啟 |
| 模組完全沒回應 | 任何指令無回應 | Hardware 頁 Reset（DTR）→ 不行就 Power 循環（RTS）＋重跑開機儀式 |
| 公共伺服器掛掉 | OPEN 類指令逾時或被拒 | 換備援伺服器（P4/P6 已列）；先 `AT+QPING` 確認不是網路問題 |
| 漫遊網路慢 | 各種逾時 | QIACT 最長 150s、QHTTPPOST CONNECT 最長 125s 都是手冊上限，等好等滿再判失敗；失敗先 `AT+QIGETERROR` |
| 頁面重載 | 重開 port = RTS 重新 assert = **模組斷電** | 必重跑開機儀式（技能檔 §2 鐵律），PDP 會自動回來 |

## §6 外部測試資源一覽

全部於 2026-08-06 從開發機實測連通（詳細數據與延遲見 `reports/tcp-server-setup.md` §3）。
⚠ **只有 `AT+QIOPEN` 的 `tcpbin.com:4242` 已寫進程式預設值（V26.0.58）**；
其餘各協定的預設值仍是舊值，等各自階段（P4／P5／P6）開跑時再改 —— 在那之前請手動填入。

| 用途 | 位址 | 帳密 | 備註 |
|---|---|---|---|
| **TCP echo** | **`tcpbin.com:4242`** | — | 原樣回送，390 ms |
| **TLS echo** | **`tcpbin.com:4243`** | — | TLSv1.2 / ECDHE-RSA-AES256-GCM；交握後 echo 已驗證 |
| TLS echo（需用戶端憑證） | `tcpbin.com:4244` | 需 client cert | 本工具無法提供憑證，僅供負面測試 |
| 任意埠連通性 | `portquiz.net:<任何埠>` | — | 判斷某個埠是否被電信商擋掉 |
| HTTP GET | **`http://www.example.com/`** | — | 200 OK；長度剛好 23 bytes，對得上手冊 `AT+QHTTPURL=23,80` 範例 |
| HTTPS GET | `https://example.com/` | — | 同上走 TLS |
| HTTP POST | `http://httpbin.org/post` | — | 回 JSON echo；80／443 皆通 |
| 純 HTTP（永不轉址） | `httpforever.com:80` | — | 200 OK；neverssl.com 實測回 **403，不可用** |
| NTP | `pool.ntp.org:123` | — | ⚠ `+QNTP` 回的時間是 UTC 卻帶本地時區標記 |
| **MQTT** | **`broker.emqx.io:1883`** | 免認證 | 406 ms，實測最快；TLS 走 8883 |
| MQTT 備援 | `broker.hivemq.com:1883` / `test.mosquitto.org:1883` | 免認證 | mosquitto 較慢（1065 ms）且有流量限制 |
| **FTP（唯讀）** | **`test.rebex.net:21`** | **demo / password** | 根目錄有 `pub/` 與 **`readme.txt`**；`STOR` 回 550；也支援 FTPS explicit |
| FTP（可寫） | `ftp.dlptest.com:21` | **`dlpuser`** / `rNrKYTX9g7z3RgJRmxWuGHbeu` | ⚠ 帳號**只能寫 `dlpuser`**，`dlpuser@dlptest.com` 實測回 530；密碼會換，見 dlptest.com/ftp-test/ |
| ~~FTP 測試檔~~ | ~~`speedtest.tele2.net:21`~~ | — | ❌ **Connection refused，服務已停止** |

**SSL 憑證驗證的負面測試站**（P5 專用，全部實測可連）——
`seclevel` 設 1／2 後，**連得上代表驗證沒生效，連不上且錯誤碼正確才算通過**：
`expired.badssl.com:443`（憑證過期）、`self-signed.badssl.com`（自簽）、
`wrong.host.badssl.com`（主機名不符，測 SNI／CN）、`untrusted-root.badssl.com`（根憑證不受信任）、
`badssl.com`（**正對照組，應成功**）。

## §7 與既有文件的關係

- 開機儀式與硬體操作：`.claude/skills/EG800K_Modem_SKILL.md` §0-§2
- 註解表擴充規則：技能檔 §3.5（六條鐵律，含「手冊沒寫的不寫」）
- 指令語法驗證方法（`=?` 探測）：技能檔 §4.6
- 盤點報告：`reports/at-command-coverage-audit.md`（本計劃結案後在其 §7 補記）

## §8 流量帳本（實測時填寫）

| 日期 | 階段 | 開始 QGDCNT（sent,recv） | 結束 QGDCNT | 本段消耗 | 備註 |
|---|---|---|---|---|---|
| 2026-08-06 | P1 第一輪 | 0,0 | 794,986 | ≈ 1.8 KB | 含 QIACT 排障重試 |
| 2026-08-06 | P1 第二輪（驗證註解） | 0,0（重開機歸零） | 554,746 | ≈ 1.3 KB | 計數器不存 NV，重開機即歸零 |
| 2026-08-07 | P5 重開機後那一段 | 0,0 | 15298,59586 | ≈ 73 KB | 11 次 TLS 交握；**只涵蓋該次開機之後** |
| 2026-08-08 | P8-1 總帳（開機後） | 0,0 | 0,0 | 0 | 見下方「為什麼沒有總計」 |

**P1 合計約 3.1 KB**（計劃預估 4 KB，實際更省）。注意：`QGDCNT` 未執行 `AT+QGDCNT=1`
存 NV，**每次模組重開機即歸零** —— 跨階段累計要自己加總。

> 註：`AT+QGDCNT?` 第一個數字是**送出**、第二個是接收（V26.0.23 註解陷阱清單）。
> 計數器預設不存 NV，模組斷電歸零 —— 所以**每段都要當場記**，不能事後補。

### 🔴 為什麼這份帳本永遠不會有「總計」一列（2026-08-08 P8-1 定案）

原計劃寫「8-1 `AT+QGDCNT?` 總帳」，隱含假設是模組某處存著一個跨重開機的累計值。
**沒有這種東西。** 2026-08-08 實測：

```
AT+QGDCNT?     → +QGDCNT: 0,0            ← 本次開機後歸零，前面幾天的量全部不見
AT+QAUGDCNT?   → +QAUGDCNT: 0
AT+QAUGDCNT=?  → +QAUGDCNT: (0,30-65535)
```

`QAUGDCNT` 名字看起來像「累計（Accumulated）」，範圍卻是 `(0,30-65535)` ——
**那是「每隔幾秒把計數器寫進 NV」的自動保存間隔（0＝關閉），不是流量數字**。
本機出廠是 0，所以從頭到尾沒有任何一次寫進 NV。

而本專案的**開機儀式每次重新整理頁面都要跑一遍**（RTS 是電源、負邏輯），
等於整個測試期間模組斷電了幾十次，`QGDCNT` 也就歸零了幾十次。

**結論：跨階段的實際總流量無法從模組取得，只能靠上表逐段記錄相加。**
上表只涵蓋當場記了的三段（P1 兩輪 3.1 KB ＋ P5 一段 73 KB），
**P2／P3／P4／P6 全程沒有當場記 QGDCNT，那部分永久遺失。**

要在後續測試拿到真總帳，唯一作法是**測試開始前先下 `AT+QAUGDCNT=30`**
（每 30 秒存一次 NV），代價是增加 NV 寫入次數。這件事**沒有做**，
現在補做也追不回已經歸零的量。

### 各階段流量：實測 vs 估算（務必分清楚）

| 階段 | 計畫預估 | 實際 | 依據 |
|---|---|---|---|
| P1 | 4 KB | **3.1 KB** | QGDCNT 實測兩輪 |
| P2 | 3 KB | 未記 | — |
| P3 | 20 KB | 未記；另有獨立估算 15–25 KB | 對端 body 大小推算，非 QGDCNT |
| P4 | 5 KB | 未跑完 | — |
| P5 | 12 KB | **≥ 73 KB**（單一次開機後那段） | QGDCNT 實測；全階段「150–200 KB」是**估算** |
| P6 | 6 KB | 未記 | — |
| P7 | 未定 | 已完成的 7-1／7-6 皆零流量 | — |
| P8 | 零流量 | 零流量 | — |

⚠ **P5 明顯超出預估**（估 12 KB、光一次開機後就 73 KB）。原因是 TLS 交握本身
就要拉整條憑證鏈，而 5-9／5-10 那組 2×5 對照做了 11 次交握。
計畫總預算「核心 < 40 KB、含重試抓 3 倍 < 200 KB」仍未突破，
但**單看 P5 一項就吃掉了核心預算的大半**。

以下數字是**應用層 payload**，與 QGDCNT（含 TCP/TLS 標頭與重傳）不是同一回事，
不要混著加：

- P5：5-4 送 15／收 15 bytes、5-7 送 16 bytes、V26.0.74 回歸 送 18／收 18 bytes；
  憑證 `AT+QFUPL` 寫入 UFS 1,939 bytes（`+QFUPL: 1939,4f64`）
- P6：LIST 目錄 1,175 bytes、PUT 上傳 20 bytes、GET `readme.txt` 379 bytes；
  6-9 逃逸測試兩個檔案各下載到 16,471 與 19,156 bytes 即中止
- P3：example.com body 559 bytes、POST 回應 440 bytes、response-headers 92 bytes、
  GETEX 分段 8+8=16 bytes

### TCP keepalive 的流量（推算，非實測）

每次探測來回約 80 bytes。`idle=30` 秒且持續閒置 → 約每小時 9.4 KB、每天 225 KB、
每月 **6.8 MB**；`idle=600` 秒 → 約每天 11 KB。
**這組數字沒有實測過**，是從探測封包大小乘以頻率推出來的，
拿來做產品決策前要自己驗一次。
