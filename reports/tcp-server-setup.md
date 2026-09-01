# 測試對端（endpoint）選擇指南 —— 從「自架 TCP server」到「免費公開服務」

> 建立：2026-08-06｜最後更新：2026-08-06｜對應：連線測試計劃 P2～P6
> 程式版本：NuModem EG800 **V26.0.58**（本文所述預設值已內建）

## 緣起（user 提問）

> 在測試 p2 tcp socket 收發的測試之前，我希望你幫我想一個辦法在我的電腦建立一個 tcp server
> 來收 tcp socket 發出的測試資料，我的網路必須經過 router 連到外網，沒有固定 ip
> —— 2026-08-06

> 有沒有不用設定 router 的 port forwarding 的方式？因爲我這個 numodem 軟體是要給各種消費者使用，
> 他們不一定能修改 reuter 的設定
> —— 2026-08-06

> 能不能請求 router 建立臨時通道（tunnel）的方式
> —— 2026-08-06

> 或是有沒有免費 tcp server 的公衆服務
> —— 2026-08-06

---

## §1 結論先講

**消費者情境下，NuModem 不該要求使用者開任何一個埠。**

理由不是「開埠很麻煩」，而是**開埠在相當比例的使用者身上根本不可能成功**，而且失敗時使用者無從診斷：

| 障礙 | 誰會遇到 | 使用者能自己解決嗎 |
|---|---|---|
| 路由器沒有管理權限（宿舍／公司／租屋） | 常見 | ✗ |
| ISP 用 CGNAT，家裡根本沒有公網 IP | 行動網路分享、部分寬頻業者 | ✗ |
| 路由器關閉 UPnP／NAT-PMP／PCP | 視機種與韌體 | 要進管理介面，等同回到手動設定 |
| 公網 IP 會變動 | 所有家用動態 IP | 要另外設 DDNS |
| Windows 防火牆擋入站 | 所有 Windows | 要按對彈窗或下 netsh |

而**這一切都是不必要的** —— 因為 `AT+QIOPEN` 本來就是 **TCP client**：模組主動往外連。
測試需要的只是「一台從外網連得到的伺服器」，不是「使用者家裡的伺服器」。
免費公開服務已經提供了這個角色，而且不必註冊、不必付費、零設定。

**V26.0.58 已把 TCP/IP 頁的 `AT+QIOPEN` 預設對端改為 `tcpbin.com:4242`。**
MQTT／SSL／FTP 的候選位址也已一併實測（§3 有完整數據），
但**尚未套用** —— 那三頁各自的測試階段還沒開跑，等做到 P4／P5／P6 再改（見 §5）。

---

## §2 「請路由器開臨時通道」的三種標準協定 —— 以及實測失敗紀錄

user 問的方向是對的：業界確實有讓程式**自動向路由器要一個有期限的對外埠**的標準協定，
BitTorrent、遊戲主機、視訊軟體都是這樣做的。共有三種：

| 協定 | 年代 | 探索方式 | 「臨時」怎麼表達 |
|---|---|---|---|
| **UPnP IGD** | 2001 | SSDP **多播** 239.255.255.250:1900 → 取裝置描述 XML → SOAP `AddPortMapping` | `NewLeaseDuration` 秒數 |
| **NAT-PMP** | 2005（Apple, RFC 6886） | **單播** UDP 閘道:5351 | 請求裡的 `lifetime` 秒數 |
| **PCP** | 2013（RFC 6887） | **單播** UDP 閘道:5351（NAT-PMP 後繼者） | 標頭的 `lifetime` 秒數 |

工具已寫好：`tools/nat_probe.py`（純標準函式庫，不需 pip install）

```
python tools/nat_probe.py              # 只探測，不改任何設定
python tools/nat_probe.py --map 5000   # 探測成功就實際要一個 5000 埠（預設 1 小時期限）
```

### 2.1 本機實測結果（2026-08-06）

```
▶ 閘道 192.168.0.4（本機來源 IP 15.0.0.20）
  ✘ NAT-PMP：無回應
  ✘ PCP：無回應
  ✘ UPnP：閘道常見埠上找不到裝置描述 → 路由器沒開 UPnP
```

最後一項是**刻意設計的交叉驗證**，值得說明清楚：

UPnP 探索走的是**多播**送出、**單播**回來 —— 回應封包的來源位址（路由器 IP）
跟我們送出去的目的位址（239.255.255.250）不一樣，
**Windows 防火牆的 UDP 狀態追蹤預設會把它當成未經請求的入站封包丟掉**。
所以「UPnP 探索沒反應」有兩種完全不同的成因，不能混為一談。

為了分辨，`nat_probe.py` 繞過多播，**直接對閘道的 11 個常見 UPnP 埠**
（1900／5000／49152-49154／2869／5431／80／8080／1780／1990）抓裝置描述 XML。
結果**全部落空** → 確定是路由器沒開 UPnP，不是防火牆擋掉多播。

### 2.2 這個結果能推論到「所有消費者」嗎？不能

**必須誠實說明**：本機的網路是非典型的 —— 預設閘道是 `192.168.0.4`（不是常見的 `.1`），
介面 IP 落在 `15.0.0.0/24`，機器上有 7 個 IPv4 位址。這看起來是軟路由／實驗室配置，
不是一般家用機。**一般消費級路由器（ASUS／TP-Link／D-Link／中華電信小烏龜）出廠多半是開著 UPnP 的。**

所以正確的結論不是「UPnP 沒用」，而是：

> **UPnP／NAT-PMP／PCP 是「有的話賺到」的加分項，不能當作產品的預設架構** ——
> 因為它會因人而異，而公開伺服器不會。

`tools/upnp_port.py`（SSDP + SOAP `AddPortMapping`／`DeletePortMapping`）
與 `tools/nat_probe.py` 都保留在專案裡，將來需要自架時可直接用。

---

## §3 免費公開測試服務總表（2026-08-06 全數實測）

延遲是**從開發機量的**，不是從模組量的 —— 只用來判斷服務是否健康，不代表模組端的 RTT。

### 3.1 TCP / TLS echo（P2、P5 主力）

| 服務 | 埠 | 用途 | 實測 |
|---|---|---|---|
| **tcpbin.com** | **4242** | **明文 TCP echo** | ✅ 390 ms，送 `NuModem\n` 原樣收回。⚠ **以行為單位**：結尾沒有 `\n`（hex `0A`）就一直緩衝不回送；⚠ **15 秒閒置逾時**會主動送 FIN |
| **tcpbin.com** | **4243** | **TLS echo** | ✅ 389 ms，TLSv1.2 / ECDHE-RSA-AES256-GCM；交握後送 `PING\n` 原樣收回 |
| tcpbin.com | 4244 | TLS + 需用戶端憑證 | ✅ 連得上（本工具無法提供用戶端憑證，僅供負面測試） |
| echo.u-blox.com | 7 | RFC 862 echo | ✅ 可用但慢（3.8 s），當備援 |
| portquiz.net | 任意埠 | **任何埠都接受連線** | ✅ 5000 埠 1.57 s／8080 埠 0.54 s。用來確認「某個埠有沒有被電信商擋掉」 |
| ~~speedtest.tele2.net~~ | 21 | ~~FTP 測試檔~~ | ❌ **Connection refused，服務已停止** |
| ~~time.nist.gov~~ | 13 | ~~daytime~~ | ⚠ 連得上但不吐 banner，不可靠 |

**echo 為什麼是最好的測試對端**：送出去的位元組原樣回來，
可以拿 `AT+QISENDEX=0,"48656C6C6F0A"` 的 hex 字串跟 `AT+QIRD` 讀回來的逐 byte 比對 ——
自架伺服器能做的「看見對方收到什麼」，echo 用往返比對一樣達成，而且不必架。

### 3.2 MQTT broker（P4）

| 服務 | 明文 | TLS | 實測 |
|---|---|---|---|
| **broker.emqx.io** | **1883** | 8883 | ✅ 406 ms／TLSv1.3。**最快，允許匿名，選為預設** |
| broker.hivemq.com | 1883 | — | ✅ 459 ms |
| test.mosquitto.org | 1883 | 8883 | ✅ 1065 ms／TLSv1.3。最有名但較慢且有流量限制 |

⚠ 三者都是**完全公開**的 broker：任何人都能訂閱你發布的主題。
測試主題請加隨機字尾（程式預設 `test/numodem`，正式測試建議改成 `test/numodem/<隨機字串>`），
**絕對不要送任何真實資料上去**。

### 3.3 FTP（P6）

| 服務 | 帳號 / 密碼 | 權限 | 實測 |
|---|---|---|---|
| **test.rebex.net** | **demo / password** | 唯讀 | ✅ 1427 ms，根目錄只有 `pub/` 與 **`readme.txt`（實測 379 bytes）**；`STOR` 回 `550 Access denied`。**選為預設** |
| **ftp.dlptest.com** | **dlpuser / rNrKYTX9g7z3RgJRmxWuGHbeu** | **可讀寫** | ✅ 342 ms 登入成功，目錄裡看得到其他使用者當天上傳的檔案 → 確認可寫。**測 `AT+QFTPPUT` 用這個** |
| ftp.gnu.org | anonymous / 任意 email | 唯讀 | ✅ 800 ms，`220 GNU FTP server ready.` |

**兩個實測到的坑**：

1. `ftp.dlptest.com` 的帳號**只能寫 `dlpuser`**；舊文件常見的 `dlpuser@dlptest.com` 已失效，實測回 `530 Login incorrect.`
2. dlptest 的密碼**會不定期更換**。連不上時去 <https://dlptest.com/ftp-test/> 查最新值，別浪費時間 debug 模組。

### 3.4 HTTP（P3）

| 服務 | 實測 |
|---|---|
| **example.com:80** | ✅ `HTTP/1.1 200 OK`。**維持預設** —— `http://www.example.com/` 剛好 23 bytes，與手冊 §3.1.1 的 `AT+QHTTPURL=23,80` 範例對得起來，是驗證「URL 不可附加 CR/LF」的現成證據 |
| httpforever.com:80 | ✅ 200 OK，永不轉址到 HTTPS |
| httpbin.org:80／:443 | ✅ 兩者皆通，需要回顯 header／狀態碼時用 |
| ⚠ neverssl.com:80 | 連得上但回 **403 Forbidden**，不適合當預設 |

### 3.5 SSL 憑證驗證的負面測試（P5 專用，全部實測可連）

`AT+QSSLCFG="seclevel"` 設 1 或 2 開啟憑證驗證後，這組是唯一能證明「驗證真的有在動」的方法 ——
**連得上代表驗證沒生效，連不上（且錯誤碼正確）才代表通過**：

| 主機（皆 :443） | 應觸發的失敗 |
|---|---|
| `expired.badssl.com` | 憑證過期 |
| `self-signed.badssl.com` | 自簽憑證 |
| `wrong.host.badssl.com` | 主機名不符（測 SNI／CN 檢查） |
| `untrusted-root.badssl.com` | 根憑證不受信任 |
| `badssl.com` | **正對照組**，應該要成功 |

---

## §4 什麼時候還是需要自架伺服器

公開 echo 覆蓋了 P2 的絕大部分，但有兩件事它做不到：

1. **主動斷線** —— 驗證模組收到 `+QIURC: "closed"`
2. **連上就主動推資料** —— 驗證模組收到 `+QIURC: "recv"` 的被動接收路徑

這兩項需要 `tools/tcp_test_server.py`：

```
python tools/tcp_test_server.py                            # 0.0.0.0:5000，echo 模式
python tools/tcp_test_server.py --no-echo                  # 只收不回（測單向送）
python tools/tcp_test_server.py --send-on-connect "hi\r\n" # 連上就主動推（測 recv URC）
python tools/tcp_test_server.py --drop-after 3             # 收 3 筆後主動斷線（測 closed URC）
```

每筆資料印出**時間／長度／ASCII／HEX 三欄對照**：

```
[22:12:11.940] ◆ 連線建立 ← 36.239.107.43:51234
[22:12:11.941]   ← 收到 6 bytes | Hello. | 48 65 6C 6C 6F 0A
[22:12:11.941]   → 回送 6 bytes（echo）
```

要讓模組連得到它，依可行性排序：

| 方式 | 需要什麼 | 適用 |
|---|---|---|
| **A. 通道服務** `bore local 5000 --to bore.pub` | 只要能上網，**不必碰路由器、不必註冊** | 首選；`ngrok tcp 5000` 同理但要免費帳號 |
| **B. 自動開埠** `python tools/nat_probe.py --map 5000` | 路由器有開 UPnP／NAT-PMP／PCP | 有就賺到，本機實測沒有 |
| **C. 手動連接埠轉發** 外部 5000 → `192.168.0.20:5000`／TCP | 路由器管理權限 ＋ 真公網 IP（本機 `36.239.107.43` 是中華電信真公網，非 CGNAT） | 開發機可行，消費者不可行 |
| **D. 租 VPS** | 月費 | 長期／異地測試才需要 |

**方式 C 的兩個注意事項**：公網 IP 會變（可用路由器內建 DDNS／DuckDNS 固定成網域名稱，`AT+QIOPEN` 吃網域名稱）；
ISP 對家用線路常封 25／135-139／445，偶爾封 80／443，**用 5000 以上高位埠最安全**。
Windows 防火牆放行：

```
netsh advfirewall firewall add rule name="NuModem TCP test 5000" dir=in action=allow protocol=TCP localport=5000
```

---

## §5 程式內建預設值：已改的與待改的

> ⚠ **範圍紀律**：本次**只動 TCP/IP 頁**。下表「待改」那些位址雖然都實測可連，
> 但屬於 MQTT／SSL／FTP 三頁，各自的測試階段（P4／P5／P6）都還沒開跑 ——
> **等做到那一階段再改**，不要提前套用。
> （2026-08-06 user 指正：「我只講到 tcp/ip 你已經做到 mqtt 和 ftp 去了，一步一步來好嗎」）

### 5.1 V26.0.58 已套用（TCP/IP 頁，僅此一處）

| 指令 | V26.0.57 之前 | V26.0.58 起 | 為什麼 |
|---|---|---|---|
| `AT+QIOPEN` | 主機 **空字串**、埠 8080 | **`tcpbin.com` : `4242`** | 空字串按下去必然失敗；改成 echo 服務，一按就能驗證往返 |

同頁的 `AT+QPING`（`8.8.8.8`）與 `AT+QIDNSGIP`（`www.google.com`）本來就可用，未動。

### 5.2 待各自測試階段開跑時再處理

| 階段 | 頁簽 | 指令 | 目前值 | 問題 | 候選 |
|---|---|---|---|---|---|
| P4 | MQTT | `AT+QMTOPEN` | 主機 **空字串** | 按下去必然失敗 | `broker.emqx.io` : `1883`（實測最快、允許匿名） |
| P5 | SSL | `AT+QSSLOPEN`（buffer／direct push） | `example.com` : 443 | 只驗得到交握，送出去的資料收不回來 | `tcpbin.com` : `4243`（TLS echo，可逐 byte 驗資料真的穿過通道） |
| P6 | FTP | `AT+QFTPOPEN` | **`192.0.2.2`** : 21 | RFC 5737 文件保留位址，從手冊照抄，**永遠連不上** | `test.rebex.net` : `21` |
| P6 | FTP | `AT+QFTPCFG="account"` | `test` / `test` | 手冊範例帳密不對應任何真實伺服器 | `demo` / `password` |
| P6 | FTP | `QFTPMDTM`／`QFTPSIZE`／`QFTPGET`×2 | `test.txt` | 測試站上不存在此檔 | `readme.txt`（實測 379 bytes 純文字） |
| P6 | FTP | `AT+QFTPPUT` | `test.txt` | 唯讀站上傳必回 550 | 檔名不變，改連 `ftp.dlptest.com` 測上傳 |

**不需要改的**：`AT+QHTTPURL` 的 `http://www.example.com/` —— 實測 200 OK，
且長度剛好 23 bytes 與手冊 §3.1.1 的 `AT+QHTTPURL=23,80` 範例對得起來，
是驗證「URL 不可附加 CR/LF」的現成證據，動了反而損失。

---

## §6 P2 開跑前檢查清單（公開服務路線）

- [ ] 模組端 PDP 已就緒（`AT+CGACT?` → `AT+CGACT=0,<cid>` → `AT+QIACT=1` → `AT+QIACT?` 有 IP）
- [ ] `AT+QIDNSGIP=1,"www.google.com"` 能解析 → 確認 DNS 通
- [ ] `AT+QIOPEN=1,0,"TCP","tcpbin.com",4242,0,0` → 等 `+QIOPEN: 0,0`
- [ ] `AT+QISENDEX=0,"48656C6C6F0A"` → `SEND OK`
- [ ] 等 `+QIURC: "recv",0` → `AT+QIRD=0,1500` → 讀回的 hex **必須逐 byte 等於** `48 65 6C 6C 6F 0A`
- [ ] `AT+QISEND=0,0` 看 acked 數字（`SEND OK` 不代表對方收到，acked 才算數）
- [ ] `AT+QICLOSE=0`

需要測 `+QIURC: "closed"` 與被動 `"recv"` 時，才改走 §4 自架路線。

## §7 相關文件

- `reports/data-connection-test-plan.md` —— P0～P8 連線測試計劃（P1 已完成）
- `tools/tcp_test_server.py` —— 自架 echo 伺服器
- `tools/nat_probe.py` —— NAT-PMP／PCP／UPnP 三協定探測與自動開埠
- `tools/upnp_port.py` —— UPnP IGD 單獨實作（SSDP 逐張網卡探索 ＋ SOAP）
