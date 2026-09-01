# P6 FTP 實測結果（EG800K）

- 日期：2026-08-07
- 韌體：`EG800KCNGCR07A06M04`
- 工具版本：NuModem EG800 V26.0.74
- 伺服器：`ftp.dlptest.com`（可寫，`dlpuser` / 當日密碼）、`test.rebex.net`（唯讀，`demo` / `password`）
- SIM：1NCE 預付卡，IP `10.187.7.8`

## 緣起（user 提問）

> 接下來測試 P6 FTP
> —— 2026-08-07

---

## §1 結論摘要

**8 項通過、1 項部分通過、1 項選測未做。** 三個發現值得記住，其中兩個推翻了既有認知。

> 6-7 於同日稍晚補做完成（user 指示「補做 6-7」），見 §2.7。

| # | 測項 | 結果 | 關鍵證據 |
|---|---|---|---|
| 6-1 | 帳密＋被動模式 | ✅ | 設定與讀回一致；**密碼被模組遮成 `*`** |
| 6-2 | 登入 | ✅ | 兩台伺服器都回 `+QFTPOPEN: 0,0` |
| 6-3 | 目錄操作 | ✅ | `+QFTPPWD: 0,"/"`、`+QFTPCWD: 0,0`、`+QFTPLIST: 0,1175` |
| 6-4 | **兩段式上傳** | ✅ | `+QFTPPUT: 0,20`，**主機端讀回內容逐 byte 相符** |
| 6-5 | 檔案屬性 | ✅ | `+QFTPSIZE: 0,20`、`+QFTPMDTM: 0,"20260807141117"` |
| 6-6 | 下載比對 | ✅ | rebex 上多次成功（含 LIST 之後）；dlptest 因資料連線失效未完成 |
| 6-7 | 改名＋刪除 | ✅ | `+QFTPRENAME: 0,0`、`+QFTPDEL: 0,0`，前後 SIZE 各自符合預期（§2.7）|
| 6-8 | 登出 | ✅ | `+QFTPCLOSE: 0,0` —— **但必須等 URC，見 §3.1** |
| 6-9 | `+++` 逃逸／`ATO` 續傳 | ⚠ 部分 | 逃逸成功；**`ATO` 無法續傳，回 `NO CARRIER`** |
| 6-10 | FTPS explicit | ⏸ 選測未做 | — |

---

## §2 逐項紀錄

### 6-1 設定（`AT+QFTPCFG`）

```
AT+QFTPCFG="account","dlpuser","<密碼>"   OK
AT+QFTPCFG="transmode",1                 OK      ← dlptest 只支援被動模式
AT+QFTPCFG="filetype",0                  OK
AT+QFTPCFG="contextid",1                 OK
AT+QFTPCFG="rsptimeout",90               OK

AT+QFTPCFG="account"
+QFTPCFG: "account","dlpuser","*************************"
```

⚠ **密碼在讀回時是被遮住的**，不是明碼。工具原本的註解寫「密碼在這行是明碼，截圖或錄影前留意」——
那句是錯的，已於 V26.0.75 更正。（設定時輸入的原文仍是明碼，那部分的提醒依然成立。）

### 6-2／6-3 登入與目錄

```
AT+QFTPOPEN="ftp.dlptest.com",21
OK
+QFTPOPEN: 0,0

AT+QFTPPWD    → +QFTPPWD: 0,"/"
AT+QFTPCWD="/" → +QFTPCWD: 0,0
AT+QFTPLIST="/","COM:"
CONNECT
-rw-r--r-- 1 1001 1001 129889 Aug 07 14:10 10.101.1.2_20260807-10110597_IVA.jpg
…
+QFTPLIST: 0,1175
```

### 6-4 兩段式上傳（核心驗收）

```
AT+QFTPPUT="numodem-test.txt","COM:",0,20,1
CONNECT
NuModem-P6-FTP-test\n          ← 送出剛好 20 bytes
OK
+QFTPPUT: 0,20
```

**驗證方式刻意不靠模組自己**：從主機端用 Python `ftplib` 連上同一台伺服器把檔案讀回來，

```python
RETR numodem-test.txt → b'NuModem-P6-FTP-test\n'   # 20 bytes，逐 byte 相符
```

這比「模組說它傳了 20 bytes」強得多 —— 它排除了「模組自己算錯」與「伺服器收到但存壞」兩種可能。

### 6-5 檔案屬性

`+QFTPSIZE: 0,20`（與 payload 長度一致）、`+QFTPMDTM: 0,"20260807141117"`。

### 6-6 下載

在 **rebex** 上完全正常，而且**重複多次、包含在 LIST 之後**都沒問題：

```
AT+QFTPGET="readme.txt","COM:"
CONNECT
Welcome to test.rebex.net! …
+QFTPGET: 0,379
```

同一 session 連做 `LIST → GET → NLST → GET → SIZE`，每次結束狀態都回到 1（閒置）。
**所以 `AT+QFTPGET` 搭 `"COM:"` 的功能本身沒有問題。**

在 dlptest 上失敗，原因見 §3.3。

---

### 6-7 改名＋刪除（補做）

第一次嘗試就整串通過，全程只走控制通道：

```
AT+QFTPPUT="numodem-67.txt","COM:",0,20,1  → +QFTPPUT: 0,20
AT+QFTPRENAME="numodem-67.txt","numodem-67b.txt"
                                          → +QFTPRENAME: 0,0
AT+QFTPSIZE="numodem-67.txt"              → +QFTPSIZE: 627,550   ← 舊名已不存在
AT+QFTPSIZE="numodem-67b.txt"             → +QFTPSIZE: 0,20      ← 新名在，大小正確
AT+QFTPDEL="numodem-67b.txt"              → +QFTPDEL: 0,0
AT+QFTPSIZE="numodem-67b.txt"             → +QFTPSIZE: 627,550   ← 已刪除
AT+QFTPCLOSE                              → +QFTPCLOSE: 0,0
```

註解逐條正確，`627,550` 還做了**兩層解碼** ——
「錯誤 627：FTP 未執行所請求的動作；伺服器回覆 550：動作未執行：檔案或目錄不存在」，
模組層與 FTP 協定層分開講，符合驗收條件。

⚠ 值得記一筆：**這次補做時，主機端（家用寬頻）對 dlptest 的資料連線仍然逾時，
而模組（行動網路）第一次就上傳成功**。再次印證 §3.3 的判斷 ——
那是路徑相關的伺服器端問題，不是模組缺陷；換條路就好了。

---

## §3 三個發現

### 3.1 ⚠ `AT+QFTPCLOSE` 是非同步的 —— `OK` 不代表關好了

這是本輪最大的坑，也讓我在測試中繞了很久的路。

```
AT+QFTPCLOSE
OK                    ← 只代表「指令收下」
…（此時狀態是 3＝正在關閉）
AT+QFTPOPEN=…
+CME ERROR: 603       ← 伺服器忙碌
AT+QFTPSIZE=…
+CME ERROR: 603
…
+QFTPCLOSE: 0,0       ← 真正關完，這時才允許下一個動作
```

**症狀極具誤導性**：一連串 603 看起來像「模組壞了」或「伺服器擋我們」，
實際上只是關閉還沒完成。正確做法是**等 `+QFTPCLOSE: 0,0` URC** 再動作，
`rsptimeout` 預設 90 秒就是這個等待的上限。

工具的按鈕說明已更新，明確寫出這件事。

### 3.2 ⚠ `+++` 是「中止」不是「暫停」，`ATO` 續不回來（與手冊不符）

手冊（FTP(S) AN v1.5 p13）寫：

> The port exits data mode after inputting +++ … and it **reenters data mode by executing ATO command**
> after AT+QFTPGET, AT+QFTPLIST and AT+QFTPNLST.

**實測不成立。** 兩次測試（16471 bytes 的檔案等 1.3 秒後逃逸、19156 bytes 的檔案只等 0.4 秒後逃逸）
結果一致：

| 步驟 | 結果 |
|---|---|
| `+++`（前後各靜默 1 秒，不加 CR） | `OK`，資料立刻停止輸出 ✔ |
| 逃逸後下 AT 指令 | 正常可用 ✔ |
| `AT+QFTPSTAT` | **`0,1`＝閒置**（若只是暫停，應該還是 2＝傳輸中） |
| `ATO` | **`NO CARRIER`** —— 沒有可回復的連線 |

狀態回到「閒置」是決定性證據：**模組把整個傳輸中止了，不是掛起**。
所以 `+++` 可以用來「從失控的資料模式脫身」，但**不能用來暫停大檔下載再續傳**。

### 3.3 dlptest 的被動資料連線不可靠 —— `+CME ERROR: 615`

```
AT+QFTPPUT=…
+CME ERROR: 615      ← 615＝FTP 開啟資料連線失敗
```

特徵：

- **控制通道完全正常** —— 登入成功、`AT+QFTPSIZE` 之類的控制指令有回應
- **資料通道打不開** —— 任何需要開資料連線的動作（PUT / GET / LIST）都失敗
- **一旦 615 發生，後續所有 FTP 指令一律 603**，直到依 §3.1 正確關閉為止
- **主機端也有同樣症狀**：Python `ftplib` 對 dlptest 的 `STOR` 與大檔 `RETR` 都會資料連線逾時，
  但小檔 `RETR` 與 `NLST` 可以成功

換句話說**這是伺服器端／網路路徑的問題，不是模組缺陷** —— 兩條完全不同的網路路徑
（家用寬頻與行動網路）出現一致的症狀。rebex 則全程零失敗。

**建議**：往後 FTP 的讀取類測試以 `test.rebex.net` 為主，
只有寫入類（PUT / RENAME / DEL）才用 dlptest，而且要**一次做完、失敗就重開機再來**。

### 3.4 模組資料堆疊退化（與 P5 同一族）

重開機後的第一個 PUT 就回 615，代表模組在多次失敗後會進入一種
「控制通道還活著、資料通道全滅」的狀態。與 P5 記錄的 552 退化不同的是這次錯誤碼更明確。
復原方式一樣：**完整開機儀式**（`AT+QFTPCLOSE` 與 PDP 重啟都救不回來）。

---

## §4 未完成的項目

| # | 為什麼沒做完 | 建議 |
|---|---|---|
| 6-10 FTPS explicit | 選測項目；P5 已證明憑證可上傳、`seclevel` 驗證有效，FTPS 只是換一層載體 | 想做的話：`AT+QFTPCFG="ssltype",2` ＋ `"sslctxid",1`，rebex 支援 explicit FTPS |

---

## §5 因本次實測而修正的程式問題

| 問題 | 原本 | 現況 |
|---|---|---|
| `AT+QFTPCFG="account"` 回應註解 | 「密碼在這行是明碼，截圖或錄影前留意」 | 更正為「密碼會被模組遮成 `*`」 |
| `AT+QFTPCLOSE` 按鈕說明 | 「登出 FTP(S) 伺服器；收到 URC 後可重新 QFTPOPEN」（太輕描淡寫） | 明確寫出「立刻回的 OK 只代表收下，期間任何 FTP 指令一律 603」 |

---

## §6 相關文件

- 測試計畫：`reports/data-connection-test-plan.md` §P6
- P5 記錄（資料堆疊退化的第一次發現）：`reports/p5-ssl-test-results.md` §4.1
- 硬體與開機儀式：`.claude/skills/EG800K_Modem_SKILL.md` §0–§2
- 手冊：`../_ref/EG800K/quectel_ecx00xeg800keg810meg91xneg915keg950a_series_ftps_application_note_v1-5.pdf`
