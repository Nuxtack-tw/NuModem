# P5 SSL raw socket 實測結果（EG800K）

- 日期：2026-08-07
- 韌體：`EG800KCNGCR07A06M04`
- 工具版本：NuModem EG800 V26.0.72
- 對端：`tcpbin.com:4243`（TLS echo）、`badssl.com` 家族（憑證驗證測試）
- SIM：1NCE 預付卡，APN 自動配發，IP `10.187.7.8`

## 緣起（user 提問）

> P4全部測完，接下來測試 P5 SSL raw socket，你先幫我測試，我要離開一下
> —— 2026-08-07

---

## §1 結論摘要

**10 個測項全數通過**，其中 5-9／5-10 這組憑證驗證測試原本被認為做不到（程式裡寫著
「本工具送不出憑證所以 seclevel 1/2 必定失敗」），實測證明那句話是錯的。

| # | 測項 | 結果 | 關鍵證據 |
|---|---|---|---|
| 5-1 | SSL 參數設定與讀回 | ✅ | 四項設定寫入後查詢式讀回完全一致 |
| 5-2 | 開 TLS 連線（buffer） | ✅ | `+QSSLOPEN: 4,0`，交握 2.0 秒 |
| 5-3 | 連線狀態 | ✅ | 11 欄全數解讀正確 |
| 5-4 | 兩段式送資料 | ✅ | `SEND OK`，0.4 秒後收到 `+QSSLURC: "recv",4` |
| 5-5 | 讀回 | ✅ | `+QSSLRECV: 15` 內容逐 byte 相符，再讀為 `0` |
| 5-6 | 關閉 | ✅ | `OK`，`AT+QSSLSTATE` 清空 |
| 5-7 | direct push 模式 | ✅ | `+QSSLURC: "recv",4,16` 後資料直接吐出 |
| 5-8 | 異常路徑（無憑證用 seclevel 1） | ✅ | `+QSSLOPEN: 4,566`，符合預期 |
| 5-9 | 壞憑證必須被拒 | ✅ | 四台全部 566 |
| 5-10 | 好憑證必須連得上 | ✅ | `badssl.com` → `+QSSLOPEN: 4,0` |

---

## §2 逐項紀錄

### 5-1 SSL 參數（`AT+QSSLCFG`）

```
AT+QSSLCFG="sslversion",1,4         OK    → 讀回 +QSSLCFG: "sslversion",1,4
AT+QSSLCFG="ciphersuite",1,0XFFFF   OK    → 讀回 +QSSLCFG: "ciphersuite",1,0XFFFF
AT+QSSLCFG="seclevel",1,0           OK    → 讀回 +QSSLCFG: "seclevel",1,0
AT+QSSLCFG="negotiatetime",1,60     OK    → 讀回 +QSSLCFG: "negotiatetime",1,60
```

### 5-2／5-3 建立連線與狀態

```
AT+QSSLOPEN=1,1,4,"tcpbin.com",4243,0
OK
+QSSLOPEN: 4,0                                    ← 2.0 秒

AT+QSSLSTATE
+QSSLSTATE: 4,"SSLClient","45.79.112.203",4243,0,2,1,4,0,"uart1",1
```

11 欄依序為：clientID 4／固定字串 `"SSLClient"`／遠端 IP／遠端埠 4243／本地埠 0／
socket 狀態 2（已建立）／PDP context 1／serverID 4／存取模式 0（buffer）／AT 埠 uart1／SSL context 1。
**本地埠回報 0**，與 TCP 的 `+QISTATE` 會給真實本地埠不同，這是模組行為，不是錯誤。

### 5-4／5-5 送收資料

payload 用 `NuModem-P5-SSL\n`（15 bytes）。**結尾的 `\n` 不能省** ——
tcpbin 是逐行 echo，沒有換行就不會回送（P2 已踩過同一個坑）。

```
AT+QSSLSEND=4,15
>
NuModem-P5-SSL                    ← 送出 15 bytes，不必送 Ctrl+Z
SEND OK
+QSSLURC: "recv",4                ← 0.4 秒
AT+QSSLRECV=4,1500
+QSSLRECV: 15
NuModem-P5-SSL
OK
AT+QSSLRECV=4,1500
+QSSLRECV: 0                      ← 緩衝已空
```

### 5-7 direct push

```
AT+QSSLOPEN=1,1,4,"tcpbin.com",4243,1     ← 末碼 1
+QSSLOPEN: 4,0
AT+QSSLSEND=4,16 → SEND OK
+QSSLURC: "recv",4,16             ← 帶長度，資料緊接在下一行
NuModem-P5-PUSH
```

與 buffer 模式的差別確認：URC 多了長度欄位，且**不必再下 `AT+QSSLRECV`**。

### 5-8 異常路徑

`seclevel=1` 但模組 UFS 內沒有任何憑證 → `+QSSLOPEN: 4,566`。
註解顯示「SSL socket 連線失敗」。符合預期。

---

## §3 5-9／5-10：憑證驗證是不是真的有在動

這是 P5 唯一有安全意義的測項，也是最容易做出假結論的一項 ——
如果只測「壞憑證連不上」，那「全部都連不上」也會通過。所以做成 **2×5 對照**。

### 3.1 先解決一個錯誤前提

程式裡原本寫著：

> seclevel 設 1 或 2 就必須先用 AT+QFUPL 把憑證上傳到模組
> —— **本工具送不出二進位檔，所以填 1/2 時交握必定失敗**

**這句話是錯的。** PEM 憑證是純 ASCII（`-----BEGIN CERTIFICATE-----` + base64），
而 `writeRaw()` 收 `Uint8Array`、任何位元組都送得出去。實測：

```
AT+QFUPL="isrgx1.pem",1939,60
CONNECT
<送出 1939 bytes 的 ISRG Root X1 PEM>
+QFUPL: 1939,4f64                 ← 位元組數與 checksum
OK
AT+QFLST="*"
+QFLST: "UFS:isrgx1.pem",1939
```

憑證來源：`badssl.com` 的鏈是 `*.badssl.com ← YR2 ← Root YR ← ISRG Root X1`（四層），
取最上層的 ISRG Root X1，存於 `reports/artifacts/badssl-root.pem`。

### 3.2 SNI 是必要條件（差點被誤判成時鐘問題）

第一次用 seclevel 1 連 `badssl.com` 得到 566。第一直覺是模組時鐘不對導致有效期檢查失敗
（這是嵌入式 TLS 最常見的死因），但查證後推翻：

```
AT+CCLK?   +CCLK: "26/08/07,13:54:02+32"      ← 時間正確
AT+QSSLCFG="ignorelocaltime",1,1 後重試 → 仍然 566   ← 排除時鐘
AT+QSSLCFG="sni",1,1 後重試             → +QSSLOPEN: 4,0   ← 就是它
```

**`sni` 出廠預設是 0。** badssl.com 同一個 IP 掛了十幾個測試網域，不送 SNI 就會拿到
不匹配的預設憑證，驗證必然失敗。這條對所有共用 IP 的 HTTPS 服務都成立。

### 3.3 2×5 對照結果

環境：`cacert="isrgx1.pem"`、`sni=1`、`ignorelocaltime=0`、`sslversion=4`，
每輪結束都跑尾端健康檢查確認模組沒有退化。

| 主機 | seclevel 0（不驗證） | seclevel 1（驗證伺服器） |
|---|---|---|
| `badssl.com`（正對照） | **連得上** `4,0` | **連得上** `4,0` |
| `expired.badssl.com` | 連得上 `4,0` | **拒絕** `4,566` |
| `self-signed.badssl.com` | 連得上 `4,0` | **拒絕** `4,566` |
| `wrong.host.badssl.com` | 連得上 `4,0` | **拒絕** `4,566` |
| `untrusted-root.badssl.com` | 連得上 `4,0` | **拒絕** `4,566` |

左欄全部連得上 → 這些主機本身是通的、TLS 交握本身沒問題；
右欄只有好憑證過關 → 拒絕確實來自憑證驗證，不是「反正都連不上」。
**兩個方向都成立，5-9／5-10 通過。**

限制：四種失敗都回同一個碼 566，**模組不區分「過期」「自簽」「主機名不符」「根不受信任」**。
要知道是哪一種只能自己推理，`AT+QIGETERROR` 也只回 `0,operate successfully`（它管的是 TCP/IP 層）。

### 3.4 ⚠ `ignorelocaltime` 出廠預設是 1（不檢查有效期）

查詢式 `AT+QSSLCFG="ignorelocaltime",1` 在動任何設定之前回的就是 `1`。
意思是**出廠狀態下，即使開了 seclevel 1，過期憑證也不會因為「過期」被擋**
（本次它仍被擋是因為 `expired.badssl.com` 的憑證同時也不在我們上傳的根之下）。
要真正檢查有效期必須明確設 `AT+QSSLCFG="ignorelocaltime",1,0`，
而且模組時鐘要對（本機靠 NITZ 自動對時，`AT+CCLK?` 顯示正確）。

---

## §4 過程中發現的模組問題

### 4.1 連續開關 SSL 連線約 20 次後，資料堆疊會整個退化

症狀：所有 `AT+QSSLOPEN` 一律回 552，連先前確認可連的 `tcpbin.com:4243` 也一樣。
關鍵鑑別 —— **連純 TCP 的 `AT+QIOPEN` 到同一台也回 552**，所以不是 SSL 的問題。

此時模組看起來完全正常：

```
AT+QSSLSTATE   → OK（沒有殘留連線）
AT+QIACT?      → +QIACT: 1,1,1,"10.187.7.8"（IP 還在）
AT+QIGETERROR  → +QIGETERROR: 0,operate successfully（沒有錯誤）
```

**`AT+QIDEACT=1` + `AT+QIACT=1` 救不回來**（`QIACT=1` 直接回 `ERROR`）。
只有完整開機儀式（RTS 斷電再上電 + DTR reset）能復原，復原後 3.3 秒收到 `RDY`。

這與 MEMORY 裡記錄的「PDP 漂移」是同一族問題，但這次拿到了更明確的鑑別方法：
**用 `AT+QIOPEN` 打同一個目標**，能區分「SSL 壞了」還是「整個資料堆疊壞了」。

⚠ **這個現象污染過本次測試的中間資料**：退化期間 `wrong.host` 與 `untrusted-root`
在 seclevel 0 下也連不上，一度讓我以為那兩台的失敗不能歸因於憑證驗證。
重開機後重測，五台在 seclevel 0 全部連得上。**§3.3 的表格是重開機後的乾淨數據。**

### 4.2 流量遠高於計畫預估

測試計畫估 P5 用 12 KB。實際光是重開機後那一段（11 次交握）就用掉：

```
AT+QGDCNT?   +QGDCNT: 15298,59586      ← TX 15.3 KB / RX 59.6 KB
```

整個 P5 約做了 30 次 TLS 交握，估計總量 **150–200 KB**。原因是每次交握都要下載完整憑證鏈
（badssl 的鏈有四層），而失敗的交握一樣要付這筆錢。1NCE 預付卡要留意。

---

## §5 因本次實測而修正的程式問題

| 問題 | 原本 | 現況 |
|---|---|---|
| `AT+QSSLOPEN` 兩條 regex 完全相同 | 第二條（direct push 說明）**永遠命中不了** | 合併成一條，依末碼分辨 0/1/2 三種模式 |
| `AT+QSSLSEND` 註解寫死 | 不論填什麼都說「clientID **4**、固定長度 **17** bytes」 | 從指令取值 |
| `AT+QSSLRECV` 註解寫死 | 一律說「clientID 4、最多 1500 bytes」 | 從指令取值 |
| `AT+QSSLCLOSE` 註解寫死 | 一律說「clientID 4」 | 從指令取值 |
| `AT+QSSLSTATE=4` regex | 只認字面 4 | 改 `\d+` |
| seclevel 說明 | 「本工具送不出二進位檔，所以填 1/2 時交握必定失敗」 | 已改正並補上 SNI 陷阱 |
| `AT+QSSLSEND` 確認對話框 | 「本工具送不出 ESC（0x1B）取消，只能關連線或重啟模組」 | 已改正 —— 原始位元組按鈕送得出 ESC |

---

## §6 模組留下的狀態（要不要清掉由你決定）

| 項目 | 值 | 說明 |
|---|---|---|
| UFS 檔案 | `isrgx1.pem`（1939 bytes） | ISRG Root X1，**刻意保留** —— 刪了就得重新上傳才能重跑 5-9／5-10。要刪：`AT+QFDEL="isrgx1.pem"` |
| `seclevel` | 0 | 已還原成預設 |
| `sni` | 1 | 非預設（原為 0），但**重開機不保存**，下次開機自動回 0 |
| `cacert` | `"isrgx1.pem"` | 同上，重開機不保存 |
| 連線 | 無殘留 | `AT+QSSLSTATE` 為空 |

---

## §7 相關文件

- 測試計畫：`reports/data-connection-test-plan.md` §P5
- 硬體與開機儀式：`.claude/skills/EG800K_Modem_SKILL.md` §0–§2
- 憑證原件：`reports/artifacts/badssl-root.pem`
- 手冊：`../_ref/EG800K/quectel_ecx00xeg800keg810meg91xneg915keg950a_series_ssl_application_note_v1-3.pdf`
