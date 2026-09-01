# P7 定位加速與網路定位 實測結果（EG800K）

- 日期：2026-08-07
- 韌體：`EG800KCNGCR07A06M04`
- 工具版本：NuModem EG800 V26.0.76
- SIM：1NCE 預付卡，IP `10.187.7.8`

## 緣起（user 提問）

> 好，進P7
> —— 2026-08-07
>
> 現在我在室內，完全沒有衛星訊號
> —— 2026-08-07
>
> 你先做P7-B QLBS／QuecLocator（Wi-Fi＋基地台網路定位）
> —— 2026-08-07

---

## §1 結論摘要

**3 項完成、2 項因室內無衛星訊號無法測、4 項卡在沒有 Quectel token。**

| # | 測項 | 結果 |
|---|---|---|
| 7-1 | AGNSS 現況記錄 | ✅ 出廠值全部記錄 |
| 7-2 | 冷啟動基準 TTFF | ⛔ 室內完全收不到衛星（`$GNGGA` 使用衛星 00 顆） |
| 7-3 | 啟用 AGNSS | ⛔ 同上 —— 沒有對照組就沒有意義 |
| 7-4 | AGNSS 下載與定位 | ⛔ 同上 |
| 7-5 | NMEA 讀取 | ◐ 語句讀得出來，但內容全空 |
| 7-6 | QLBS 組態現況 | ✅ 七個子項與出廠值全部記錄；**token 確認為空** |
| 7-7 | 取得並設定 token | ⛔ **token 要向 Quectel 申請，這件事只有你能辦** |
| 7-8 | 定位查詢 | ⛔ 同上 |
| 7-9 | 熱點數量對精度的影響 | ⛔ 同上 |
| 7-10 | 室內可用性驗證 | ⛔ 同上 |
| 7-11 | 按鈕與註解 | ✅ **已完成**（V26.0.76）—— token 一到手就能直接開測 |

---

## §2 P7-A AGNSS

### 7-1 出廠現況（零流量）

```
AT+QGPS?                   → +QGPS: 0                              GNSS 關閉
AT+QGPSCFG="apflash"       → +QGPSCFG: "apflash",1                 AP-Flash 快速熱啟動：開
AT+QAGPS?                  → +QAGPS: 0                             AGNSS：停用
AT+QGPSCFG="gnssconfig"    → +QGPSCFG: "gnssconfig",8              GPS+BDS+GLONASS
AT+QGPSCFG="outport"       → +QGPSCFG: "outport","usbnmea"         ⚠ 見下
AT+QAGPSCFG?               → +QAGPSCFG: 1,http://agnss.asrmicro.com/asr-filedownload/filedown/allstar,Quectel,Quectel,9w68sauaFh000,
```

與測試計畫的預期完全吻合（apflash=1、AGNSS=0、伺服器 asrmicro allstar）。

⚠ **`outport` 是 `"usbnmea"`**：NMEA 原始資料流走 USB 埠，不是本工具用的 uart1。
所以 AT 口拿 NMEA 只能用 `AT+QGPSGNMEA` 逐句抓，看不到自動輸出的連續流。

### 7-2／7-4 為什麼沒做

user 明確告知「現在我在室內，完全沒有衛星訊號」，實測也印證：

```
AT+QGPS=1                  → OK ／ +QGPS: "firmware",0,0（GNSS 韌體載入成功）
AT+QGPSGNMEA="GGA"         → $GNGGA,,,,,,0,00,127.00,,,,,,*62
                              ↑ 定位品質 0＝無定位、使用衛星 00 顆、HDOP 127（無效值）
```

7-2 是「冷啟動基準時間」，本來就是給 7-4 當**對照組**用的。
沒有天空視野時兩者都定不出來，測了也只會得到「兩邊都失敗」——
那正是 P5 學到的教訓：**沒有可用的對照組就不要下結論**。

**要補做的話**：把模組拿到窗邊或戶外，先跑 7-2（`AT+QGPS=1` 後輪詢 `AT+QGPSLOC=2` 記 TTFF），
再 `AT+QAGPS=1` → **重開機** → 跑 7-4 比對。user 先前實測冷啟動曾超過 10 分鐘，要留時間。

### 7-5 NMEA 讀取（部分）

`AT+QGPSGNMEA="GGA"` 讀得出語句、註解也解得正確（「GGA：無定位；使用衛星 00 顆」），
但沒有衛星就沒有 GSV 內容可看，衛星圖也無從驗證。

⚠ 另記一筆：**`AT+QGPSEND` 之後再下 `AT+QGPSGNMEA` 會回 `+CME ERROR: DSAT_CME_GNSS_SE_NOT_ACT`**
（GNSS 工作階段未啟用）。目前註解只是照唸這個代號，沒解釋 —— 已列入 TODO。

---

## §3 P7-B QuecLocator（QLBS）

### 3.1 ⚠ 本機收錄的 16 份 Quectel PDF 裡，一個字都沒提到 QLBS

逐份掃過確認：QuecLocator 另有專屬應用文件，本專案的 `../_ref/` 沒有收錄。
因此下面所有敘述**只寫實測到的事實**，從子項名稱推得的語意一律標「推測」。
（HTTPS 手冊裡也有個 702，但那是 HTTP 的「逾時」，不同命名空間，不要混用。）

### 3.2 7-6 出廠組態（零流量）

`AT+QLBSCFG=?` 回七個子項：

| 子項 | 範圍 | 本機出廠值 | 備註 |
|---|---|---|---|
| `asynch` | (0,1) | 0 | 同步／非同步（推測） |
| `timeout` | (10-120) | 60 | 查詢逾時秒數 |
| `server` | 字串 | `www.queclocator.com:80` | |
| `token` | 字串 | **空** | ⚠ 卡關點 |
| `timeupdate` | (0,1) | 0 | 讀回鍵名是 `timeUpdate` |
| `withtime` | (0,1) | 0 | 讀回鍵名是 `withTime` |
| `latorder` | (0,1) | 0 | 讀回鍵名是 `latOrder` |

**⚠ 設定用小寫鍵、模組讀回卻是駝峰**（`latorder` → `latOrder`），
寫解析器時要記得轉小寫比對，否則查詢回應會對不上。

另外：`AT+QLBSCFG="ver"` 回 `ERROR`（不是有效子項）、`AT+QLBSEX` 也不存在。

### 3.3 沒有 token 時的實際行為（7-7 的實證）

```
AT+QLBS                                    → +QLBS: 702
AT+QLBSCFG="token","NUMODEM-PLACEHOLDER"   → OK          ← 設定路徑本身可用
AT+QLBSCFG="token"                         → +QLBSCFG: "token","****************"
AT+QLBS                                    → +QLBS: 702  ← 假 token 也是 702
AT+QLBSCFG="token",""                      → OK          ← 已還原成空值
```

三件事：

1. **沒 token 和 token 無效都回同一個碼 702** —— 從回應無法分辨是哪一種
2. **token 讀回時被模組遮成 `*`**，跟 FTP 密碼一樣（P6 也發現同樣行為）
3. **設定路徑本身是通的** —— 只差一串真的 token

### 3.4 7-11 按鈕與註解（已完成）

Wi-Fi Scan 頁新增「QuecLocator (QLBS)」群，14 個項目涵蓋全部七個子項的查／設，
外加 `AT+QLBSCFG=?` 與 `AT+QLBS`。回應註解涵蓋：

- `+QLBSCFG: "<key>",<value>` —— 走既有的 `cfgNote()`，會處理駝峰鍵名
- `+QLBS: <單一數字>` —— 錯誤碼，702 另附實測說明
- `+QLBS: 0,<多欄>` —— 定位成功，**但明講「本機無 token 未能實測，欄位對應待確認」**

**token 一到手就能直接開測 7-8～7-10**，不必再改程式。

---

## §4 你要辦的事

**向 Quectel 申請 QuecLocator token。** 這是 7-7～7-10 唯一的卡關點，我做不了。

拿到之後的驗證流程（工具已備妥）：

1. Wi-Fi Scan 頁 → QuecLocator 群 → `Set Token` 填入 → 送出
2. `Token?` 確認有值（會顯示成 `*`）
3. TCP/IP 頁 `Act PDP` 確認 IP 已配發
4. `Locate` → 應回 `+QLBS: 0,<座標…>`
5. 7-9：先用 Wi-Fi Scan 把 `maxbssid` 調到 10 再測，比較精度差異
6. 7-10：在 GNSS 定不出來的室內位置跑 —— **這是 QLBS 的核心價值**

---

## §5 因本次實測而修正的程式問題

| 問題 | 說明 |
|---|---|
| i18n 匯出用「欄位白名單」 | 漏收過 `optionLabels`／`placeholder`／`timeout`／`stateLabel`／`terminatorName`。已改成**窮舉所有字串屬性** |
| `L('a' + 'b')` 抽取器抓不到 | 抽取器的 regex 要求字串後面緊跟 `)`。已把該處併成單一字面值，並在 `tools/i18n_extract.py` 補上警語 |
| 沒有中文字元的模板被過濾掉 | `QuecLocator token＝{0}` 因為不含漢字而被 cjk 過濾器擋掉，改寫成「QuecLocator 的 token＝{0}」 |

---

## §6 相關文件

- 測試計畫：`reports/data-connection-test-plan.md` §P7
- P5／P6 記錄：`reports/p5-ssl-test-results.md`、`reports/p6-ftp-test-results.md`
- 硬體與開機儀式：`.claude/skills/EG800K_Modem_SKILL.md`
- ⚠ QuecLocator 的官方應用文件**不在** `../_ref/EG800K/`，取得後應補進去


---

## 2026-08-08 追測：AGNSS 開了卻沒有效果 —— 兩個獨立原因

> **緣起（user 提問）**
>
> > 我在測試 agps 加速定位，你幫我看終端機裏面我執行的命令是否有錯誤？
> > 我感覺不到 agps 加速定位的效果 —— 2026-08-08

### 結論：AGNSS 從頭到尾沒有作用過，而且就算作用了現在也測不出來

**原因一：沒有啟用 PDP context，輔助資料下載不了（致命）**

| 查驗 | 結果 | 判讀 |
|---|---|---|
| `AT+QAGPS?` | `+QAGPS: 1` | AGNSS **已啟用**、已寫 NVRAM |
| `AT+QAGPSCFG?` | `1,http://agnss.asrmicro.com/...,Quectel,Quectel,9w68sauaFh000,` | 伺服器與 token 都在，設定沒問題 |
| `AT+QIACT?` | **只回 `OK`，沒有 `+QIACT:` 行** | 🔴 **沒有任何 PDP context 啟用** |
| `AT+CGATT?` | `+CGATT: 1` | 已附著封包域 —— 但**附著 ≠ context 啟用**，容易誤判 |
| `+QGPS: "agps",…` URC | 整段 120 行從未出現 | ⚠ **不能當證據** —— 見下方「URC 缺席不代表沒下載」 |

GNSS 應用筆記 §2.3.6 的 NOTE 明載 **AGNSS 要先有已啟用的 PDP context**
（本專案 `reports/gnss-ttff-acceleration.md` §2 方案 B 也記了這一條）。
`AT+QAGPS=1` 只是把旗標寫進 NVRAM，**模組沒有資料通道就靜靜地什麼都不做**，
不會報錯 —— 這就是「設定看起來都對、卻感覺不到效果」的來源。

⚠ **`+CGATT: 1` 是這次最容易誤導人的一行。** 附著封包域只代表網路層註冊完成，
Quectel 的協定堆疊還要 `AT+QIACT=1` 才會真的有 IP。判斷資料通道通不通要看 `AT+QIACT?`。

**原因二：室內 0 顆衛星，AGNSS 本來就救不了（同樣致命）**

```
AT+QGPSGNMEA="GGA" → $GNGGA,,,,,,0,00,127.00,,,,,,*62
                                 ↑ ↑  ↑
                       定位品質 0 │  HDOP 127（無解）
                          使用衛星 00 顆
AT+QGPSLOC=2 ×3    → +CME ERROR: DSAT_CME_GNSS_NOT_FIXED_NOW
```

**AGNSS 省掉的是「用 50 bps 慢慢解調星曆」那一段，它不能無中生有衛星訊號。**
可見衛星 0 顆時無論 AGNSS 開不開都不會定位。
**AGNSS 的效果只能在看得到天空的地方量。**

### 指令本身的三個問題（都不是主因，但要知道）

1. **第一輪 `AT+QGPS=1` 下在 `AT+QAGPS=1` 之前。** 順序反了 —— 但 `QAGPS` 本來就是
   **重開機才生效**，而中間確實重開了，第二輪順序（QAGPS → 重開 → QGPS）是對的。
   實際沒造成傷害。
2. **`+CME ERROR: 505`（GNSS session 未啟用）** —— 重開機後 GNSS 是關的，
   卻在 `AT+QGPS=1` 之前就問 `AT+QGPSGNMEA="GSV"`。無害，但提醒：
   **每次重開機都要重新 `AT+QGPS=1`**（本專案 RTS＝電源，重載頁面就等於重開機）。
3. **`AT+QGPSCFG="gnssconfig"` 讀回 1（GPS+BDS）** —— 2026-08-07 記錄是 **8**
   （GPS+BDS+GLONASS，技能檔 §4）。星座變少＝可見衛星變少。室內反正沒訊號，
   但**出門測之前建議設回 8**。

### 附帶：apflash 這次也等於沒作用

`apflash` 出廠即為 1，機制是「**把上次定位得到的星曆存進 flash，下次開機匯入**」。
但**從來沒有定位成功過，flash 裡就是空的** —— 沒有星曆可匯入，自然也沒有加速。
apflash 要先有一次成功定位才會開始發揮作用。

### 下次要驗 AGNSS 的正確順序

`QAGPS` 已經是 1 且寫進 NVRAM 了，**不用再設**。到看得到天空的地方，然後：

```
1. 跑完整開機儀式                         ← RTS 是電源，這步不能跳
2. AT+QIACT=1                             ← 🔴 關鍵，先把資料通道打開（會產生流量，漫遊卡注意）
3. AT+QIACT?                              ← 確認有 +QIACT: 1,1,1,"<IP>" 才算數
4. AT+QGPSCFG="gnssconfig",8              ← 拿回三星座（可選）
5. AT+QGPS=1
6. 盯著看有沒有 +QGPS: "agps",...          ← 有這條才代表輔助資料真的下載了
7. 每 10 秒 AT+QGPSLOC=2，記錄第一次成功的時間
```

**對照組**：同一地點、`AT+QAGPS=0` ＋ 重開機，重跑一次記 TTFF。
兩邊的差才是 AGNSS 的效果 —— 只跑開啟組是量不出東西的。


### 🔴 同日實測：補上 PDP 之後，AGNSS 立刻生效（我代跑）

user 問「你不能自己重開 modem 嗎」，於是由我跑完整程序。
**輔助資料下載不需要看得到天空**，所以「AGNSS 到底有沒有在動」室內就驗得完，
只有 TTFF 比較需要出門。

程序：開機儀式（5.5 秒到 `RDY`）→ `ATE1` → `AT+CMEE=2` → `AT+QIACT=1` →
`AT+QGPSCFG="gnssconfig",8` → `AT+QGPS=1`。

`AT+QIACT?` 回 `+QIACT: 1,1,3,"10.100.167.33","2401:E180:8873:78A0:8C83:39A8:C15C:304A"`
（IPv4v6 都拿到），資料通道確實打開了。

**三項獨立證據顯示輔助資料真的下載了：**

| 證據 | 數據 | 判讀 |
|---|---|---|
| 流量 | `+QGDCNT: 0,288` → `4790,60533`，即 **TX 4.8 KB／RX 59 KB ≈ 64 KB** | 量級正好是 AGNSS 輔助資料檔（`gnss-ttff-acceleration.md` §3 預估「數十 KB」）|
| 衛星位置 | GSV 回 **38 顆**：GPS 15、GLONASS 7、BeiDou 16，**仰角／方位角全部有值、SNR 全部 `00`** | 🔴 **「知道衛星在哪，但一顆都聽不到」—— 這是 AGNSS 生效的指紋**。位置來自下載的星曆，不是從 50 bps 訊號解調來的 |
| 時間注入 | 先前 `$GNGGA,,,,,,0,00,127.00`（無時間）→ 現在 `$GNGGA,092859.000,,,,,0,00,127.00` | UTC 時間被注入，也是輔助資料的一部分 |

對照 user 那一輪（沒有 PDP）：GSV 完全空白、GGA 也沒有時間。**差別就是 `AT+QIACT=1`。**

`AT+QGPSLOC=2` 仍回 `DSAT_CME_GNSS_NOT_FIXED_NOW` —— **38 顆的 SNR 全是 00，室內是真的一點訊號都收不到**，
這與 AGNSS 無關，符合預期。

### ⚠ 訂正：URC 缺席不代表沒下載

先前這份報告寫「`+QGPS: "agps"` URC 從未出現 → 佐證輔助資料下載從未發生」，**那是錯的推論**。
補上 PDP、下載明明發生了（上表三項證據）之後，那條 URC **照樣沒有出現**。

結論：**`+QGPS: "agps"` 在本機韌體上不會發出，不能拿來判斷 AGNSS 有沒有運作。**
（該註解規則是依應用筆記寫的，不是實測來的。）
**要判斷 AGNSS 有沒有動，看這三個：`AT+QGDCNT?` 的流量增量、GSV 有沒有一堆 SNR=00 的衛星、GGA 有沒有時間。**

### 還沒做的：TTFF 對照組（需要天空視野，只有 user 能做）

現在模組已經是「有星曆、缺訊號」的狀態。到窗邊或戶外之後：

- **實驗組**（現況即是）：`QAGPS=1` ＋ PDP 已啟用 → 記錄第一次 `AT+QGPSLOC=2` 成功的時間
- **對照組**：`AT+QAGPS=0` → 重開機 → **不要**啟用 PDP → 同一地點重測

兩邊的差才是 AGNSS 的效果。⚠ 期間**不要重載頁面**（RTS 是電源，重載＝斷電＝星曆全丟）。


---

## 2026-08-29 追測：AGNSS TTFF 對照實驗 —— 冷啟動 95 秒 → 52 秒

> **緣起（user 提問）**
>
> > 我現在裝上很強的主動式GNSS天線，已經可以抓到座標資訊……回到我們未完成的agnss的測試 —— 2026-08-29
>
> 條件終於齊了：主動式天線收得到訊號（同日已定位成功並順帶修好地圖，V26.0.80）。
> 全程由 Claude 經 UI 自動執行，user 免動手。

### 結果總表

| 輪次 | 條件 | 首次回報座標 | **首次真定位（nsat>0）** | 衛星數 / HDOP |
|---|---|---|---|---|
| A0 | AGNSS 開＋apflash 殘留（約 2 小時前的星曆） | — | **24.9 秒** | 9 / 4.38 |
| **A1** | **冷啟動＋AGNSS**（apflash=0、斷電重開、PDP 已啟） | 19.9 秒（偽） | **51.5 秒** | 27 / 0.98 |
| **B** | **冷啟動、無 AGNSS、無 PDP**（純對照組） | 從未出現偽定位 | **95.0 秒** | 17 / 3.51 |

**AGNSS 讓冷啟動 TTFF 從 95.0 秒縮到 51.5 秒（−46%）**，
另外約 20 秒就先給出一筆粗略參考位置（見下方陷阱）。
量測解析度 ±5 秒（輪詢週期）。三輪都在同一地點、同一天線、半小時內完成。

### 實驗設計要點

- **「冷啟動」用 `apflash=0` ＋ 斷電達成**，不是用 `AT+QGPSDEL` ——
  因為後者根本不能用（見下）。本機 RTS＝電源，斷電即失 RAM 星曆；
  apflash 關掉後 flash 也不會回灌，這是兩份官方文件都有依據的做法（GNSS 筆記 §2.3.1.6）
- 對照組**連 PDP 都不啟用**（`AT+QIACT?` 確認無 context），杜絕任何輔助資料下載
- A0 不能當實驗組：當時 `QGPSDEL=0` 失敗、apflash 還開著，
  約 2 小時前的星曆可能殘留（筆記寫有效 1 小時，但 GPS 廣播星曆實際可用約 4 小時）。
  它的價值是呈現「**日常重複使用**」情境 —— AGNSS＋殘留星曆可到 25 秒級

### 🔴 陷阱一：`AT+QGPSDEL` 是半實作殘根，完全不能用

| 指令 | 回應 |
|---|---|
| `AT+QGPSDEL=?` | `+QGPSDEL: (0-2)` ← 看起來支援 |
| `AT+QGPSDEL=0`／`=1`／`=2` | **全部 `+CME ERROR: DSAT_CME_GNSS_INVALID_PARA`** |

且 **AT 手冊（216 頁）與 GNSS 筆記（48 頁）都沒有收錄這條指令**（pypdf 全文搜尋確認）。
`=?` 有回應不代表指令能用 —— 這是 §4.6「`=?` 是最便宜的規格書」的第一個反例，
探測完至少還要試打一次真參數。

### 🔴 陷阱二：AGNSS 會先回一筆「偽定位」，欄位看起來像成功

A1 開始後 19.9 秒，`AT+QGPSLOC=2` 回了：

```
+QGPSLOC: 113644.00,22.8xx,120.2xx,0.00,0.0,1,,3.464,1.898,290826,00
                                        ↑    ↑  ↑                      ↑
                                   HDOP 0.00 │ fix=1            nsat=00 顆
                                          高度 0.0
```

**零顆衛星卻有座標** —— 這是 AGNSS 輔助資料裡的參考位置注入，不是量測結果。
座標離真實位置約 20 公尺（本例準得反常，別指望每次都這樣）。
**判別真定位的條件：`nsat > 0` 且 `fix ≥ 2` 且 `HDOP > 0`。**
寫自動化或產品邏輯時不能只看「`+QGPSLOC:` 有沒有回東西」。
對照組 B 從頭到尾沒出現過偽定位，佐證它確實來自 AGNSS。

### 流量帳

| 項目 | 量 |
|---|---|
| A0 AGNSS 下載 | ≈ 34 KB（QGDCNT 288 → 3952,30560）|
| A1 AGNSS 下載 | ≈ 32 KB（QGDCNT 288 → 3672,28847）|
| B | **0**（無 PDP）|
| 合計（含 QIACT 開銷） | **≈ 66 KB** |

AGNSS 每次冷啟動下載約 32-34 KB —— 換算：**多花 33 KB 流量，省 43 秒**。
以 1NCE 終身 500 MB 計，每天一次冷啟動可用約 40 年，流量不是顧慮。

### 附帶收穫

- 三輪定位共 8 筆真實座標進了 `locHistory`，**地圖頁全程正常**（磚圖、標記、軌跡）——
  V26.0.80 的 `L` 遮蔽修正首次以真實資料驗證通過
- A1 用了 27 顆衛星（B 只有 17）：有星曆在手，追到的衛星都能立刻參與解算 ——
  這也是 AGNSS 的 HDOP（0.98）遠優於對照組（3.51）的原因

### 測後狀態（已復原）

`QAGPS=1`、`apflash=1` 都已寫回 NVRAM。
⚠ **`QAGPS` 重開機才生效** —— 本次 session 剩餘時間 AGNSS 實際是關的，
下次開機儀式後自動恢復啟用。gnssconfig 維持 8（三星座）。


---

## 2026-08-29 更正：QLBS 的 702 是「逾時」不是「token 無效」—— 我們誤判了三週

> **緣起（user 提問）**
>
> > QuecLocator 如何申請？ —— 2026-08-29

查申請方式時順手翻了官方應用文件，結果推翻了本報告 2026-08-07 的結論。

### 🔴 更正：舊記錄錯在哪

**舊記錄（2026-08-07）**：
> 沒 token 與假 token 都回 `+QLBS: 702` —— 從回應分不出是哪一種

**兩點都是錯的。** 官方文件（QuecLocator Application Note，`<time>` 參數說明）明載：

> `<time>` Integer type. The maximum waiting time for data from the server.
> **If no data come from the server within this interval, the command times out
> and error code 702 is returned.** Range: 10–120. Default value: 60. Unit: second.

**702 ＝ 伺服器在逾時時間內沒有回應**（就是 `AT+QLBSCFG="timeout"` 那個值），
與 token 無關。而 2026-08-07 測試時**沒有啟用 PDP context** ——
模組根本連不到 `www.queclocator.com`，當然逾時。

**這與同期 AGNSS 失敗是同一個根因**（見本報告 2026-08-08 節）：
那天我們一口氣誤判了兩個功能，原因都是「忘了 `AT+QIACT=1`」。

### 同日對照實驗（token 全程為空，唯一變因是 PDP）

| PDP | `AT+QLBS` 回應 | 意義 |
|---|---|---|
| **未啟用** | `+QLBS: 702` | 伺服器沒回應 —— **網路問題** |
| **已啟用**（`+QIACT: 1,1,3,"10.216.22.68",…`） | **`+QLBS: 10002`** | **伺服器回應了**：token 不存在 |

**結論反轉：QuecLocator 服務本身從臺灣／這張 1NCE 卡是通的**，
伺服器正常應答，缺的只有 token。拿到 token 就能直接用 —— 這比原本的判斷樂觀得多。

### 官方錯誤碼表（`+QLBS: <err>`，本次從應用文件取得）

| 碼 | 意義 |
|---|---|
| 10000 | 定位失敗 |
| 10001 | IMEI 不合法 |
| **10002** | **token 不存在** ← 本機現況 |
| 10003 | 同一 token 的裝置數超過上限 |
| 10004 | 同一裝置單日定位次數超過上限 |
| 10005 | 同一 token 的總定位次數超過上限 |
| 10006 | token 已過期 |
| 10007 | 伺服器不接受此 IMEI |
| 10008 | 同一 token 單日定位次數超過上限 |

⚠ 另註：QuecLocator 走 HTTP，**若回的是 HTTP 錯誤碼要查 HTTP 文件** ——
這解釋了先前記錄的「702 命名空間衝突」：702 本來就是 HTTP 層的逾時碼，
兩邊指的是同一件事，不是巧合撞號。

### 怎麼申請 token

**沒有自助註冊入口** —— 官方文件明寫：

> Please contact Quectel Technical Supports to apply for the token value.

且 QuecLocator 是**收費的加值服務**（value-added function, service fees collected），
不是免費 API 金鑰。管道：

| 管道 | 位址 |
|---|---|
| 技術支援（申請 token 走這裡） | http://www.quectel.com/support/technical.htm ／ support@quectel.com |
| 業務（談收費與方案） | http://www.quectel.com/support/sales.htm ／ info@quectel.com |
| QuecLocator 產品頁 | https://iot.quectel.com/doc_getStart.html#QuecLocator |

申請時建議附上：模組型號（EG800K）、韌體版本（`EG800KCNGCR07A06M04`）、
IMEI（`AT+GSN`）、用途與預估裝置數／查詢量。
⚠ **IMEI 是識別依據**（錯誤碼 10001／10007 都與 IMEI 有關），
token 很可能綁定裝置，換模組要確認是否要重新申請。

### 文件已收進專案

`../_ref/EG800K/Application Note/quectel_ec200u_eg915u_series_queclocator_application_note_v1-0__NOT-EG800K.pdf`

⚠ **檔名帶 `__NOT-EG800K` 是刻意的**：這份文件的適用機型是 **EC200U／EG915U**，
不含 EG800K。指令語法與錯誤碼與本機實測相符（`QLBSCFG` 七個子項、10002 等），
但**引用前要意識到它不是本機的官方文件** —— 比照 `../_ref/` 目錄裡 RF FTM 那份的處理慣例。
