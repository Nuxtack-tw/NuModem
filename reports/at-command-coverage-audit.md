# EG800K AT 指令覆蓋率盤點報告

> 專案：NuModem EG800（V26.0.21）
> 盤點日期：2026-08-02
> 盤點對象：`../_ref/EG800K/` 全部技術文件 vs 工具現有 66 顆指令按鈕
> 產出：413 條指令形式的逐條判定 + 行動清單

---

## 緣起（user 提問）

> **2026-08-02**
> 「NETWORK指令組是不是沒有把AT Command手冊中所有的指令都做出來？」

初步查證後回覆：NETWORK 組只涵蓋手冊第 6 章 9 條中的 4 條、第 10 章 18 條中的 2 條，
共 6/27。並說明成因是「依實用度篩選，但從未把章節整個列出來逐條裁決」。
接著提出三個選項，user 裁示：

> 「照你建議地做」（= 選項 b：先做一次全六組的完整盤點報告，看過再決定每組要收哪些）

本報告即為該裁示的產出。

---

## §1 盤點範圍與方法

### 1.1 為什麼範圍比預期大

盤點前清點 `../_ref/EG800K/`，發現目錄內有 **16 份 PDF**，而非專案文件長期記載的「7 份」。
其中包含數份我們從不知道存在的應用筆記 —— 特別是 **MQTT 應用筆記**：
現有 MQTT 頁當初是靠實機 `=?` 逐條逆推出來的，因為當時認定「ref 沒有 MQTT 文件」。

### 1.2 涵蓋的文件

| # | 文件 | 檔名標示版本 | PDF 封面實際版本 | 盤點條數 |
|---|---|---|---|---:|
| 1 | AT 指令手冊（12 章、216 頁） | v1.4 | v1.4 | 132 |
| 2 | GNSS 應用筆記 | v1-0 | **v1.1** | 51 |
| 3 | TCP/IP 應用筆記 | v1-4 | v1.4 | 70 |
| 4 | MQTT 應用筆記 | v1-5 | **v1.6** | 40 |
| 5 | Wi-Fi Scan 應用筆記 | v1-1 | **v1.2** | 6 |
| 6 | SSL 應用筆記 | v1-3 | **v1.4** | 25 ＊ |
| 7 | HTTP(S) 應用筆記 | v1-6 | **v1.7** | 20 ＊ |
| 8 | FTP(S) 應用筆記 | v1-5 | **v1.6** | 28 ＊ |
| 9 | 低功耗模式應用筆記 | v1-1 | **v1.3** | 13 |
| 10 | RF FTM 應用筆記 | v1-2 | **v1.3** | 11 |

＊ SSL / HTTP(S) / FTP(S) 由同一個 agent 一併盤點，§2 表格中合計為 90 條
（25 + 20 + 28 = 73 條自有指令，另加 12 條三份文件明文引用但定義在其他手冊的外部指令，以及 5 條跨文件重複計列）。

**警告：檔名的版本號一律不可信**，10 份裡有 7 份與封面版本不符。引用時請以 PDF 封面 Version 欄為準。

### 1.3 判定標準

每條指令四選一，判定基準是「對一個**用 UART 接 AT 口、手動下指令做功能驗證**的工程師有沒有用」。
本工具走串列 AT 口，不是 USB 網卡、不跑 QuecOpen、不做量產測試。

- **已收錄** —— 現有 66 顆按鈕已涵蓋
- **建議補** —— 明顯有用，應該做
- **可選** —— 特定情境才用，可延後
- **不建議** —— 危險 / legacy / 與現有重疊 / 本工具情境用不到（**逐條寫明理由，不略過**）

方法上採 9 個平行 agent 各負責一份文件或章節區段，全部要求「範圍內每一條都要列出」，
並強制標註副作用（重開機／關機／使 AT 口失效／清除設定／長時間阻塞／耗流量／寫 NVRAM）。

---

## §2 覆蓋率總覽

本次盤點涵蓋 **9 份文件 / 413 條指令形式**（同一指令的查詢式與寫入式分列）。

| 判定 | 條數 | 意義 |
|---|---:|---|
| 已收錄 | 68 | 工具現有 66 顆按鈕已涵蓋 |
| **建議補** | **110** | 對「UART 手動下指令做功能驗證」明顯有用 |
| 可選 | 138 | 特定情境才用，可延後 |
| 不建議 | 97 | 危險 / legacy / 與現有重疊 / 本工具用不到 |

### 各文件的覆蓋情形

| 文件 | 已收錄 | 建議補 | 可選 | 不建議 | 合計 |
|---|---:|---:|---:|---:|---:|
| AT 手冊 §1-5 | 11 | 16 | 18 | 21 | 66 |
| AT 手冊 §6-10 | 6 | 8 | 15 | 32 | 61 |
| AT 手冊 §11-12 | 2 | 1 | 2 | 0 | 5 |
| GNSS AN | 15 | 7 | 22 | 7 | 51 |
| TCP/IP AN | 19 | 17 | 25 | 9 | 70 |
| MQTT AN | 11 | 9 | 14 | 6 | 40 |
| Wi-Fi Scan AN | 4 | 0 | 1 | 1 | 6 |
| SSL / HTTPS / FTPS AN | 0 | 43 | 35 | 12 | 90 |
| 低功耗 + RF FTM AN | 0 | 9 | 6 | 9 | 24 |
| **合計** | **68** | **110** | **138** | **97** | **413** |

## §3 建議補的指令（依建議頁簽）

> 這是本報告的**行動清單**。`risk` 欄非空者代表有副作用，做成按鈕時要在說明文字警告。

### Hardware（16 條）

**ADC**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QADC` | 讀取指定 ADC 通道的電壓值（mV） | 11.5 | 300 ms | — |

**Power**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QSCLK=0` | 禁止模組進入睡眠（回到常醒狀態） | LPM §4.1.2 / AT手冊 §11.3 | 300 ms | — |
| `AT+QSCLK?` | 查詢目前是否允許模組進入睡眠 | LPM §4.1.2 / AT手冊 §11.3 | 300 ms | — |

**Serial**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT&C` | 設定 DCD 腳的行為模式 | 3.1 | 300 ms | 設定可被 AT&W 存檔；設 0 後 DCD 恆為 ON，訊號列的 DCD 指示將失去診斷意義 |
| `AT&D` | 設定模組對 DTR 由低轉高的反應 | 3.2 | 300 ms | 設 2 時 DTR 拉高會直接掛斷資料連線並停用自動接聽；設定可被 AT&W 存檔 |
| `AT&F` | 把 AT 指令設定重設為出廠預設值 | 2.10 | 300 ms | 會把 ATE/ATQ/ATV/AT&C/AT&D/AT+IFC 等一次打回預設（預設 E:1 開回顯），終端機的回顯行為… |
| `AT&V` | 一次列出所有單字母 AT 參數的目前值 | 2.11 | 300 ms | — |
| `AT+IFC` | 查詢／設定 UART 硬體流控（RTS/CTS） | 3.3 | 300 ms | 設 2,2 但主機端未接或未啟用 RTS/CTS，模組會因等不到 CTS 而停止送資料，AT 口看起來像當掉 |
| `AT+IPR` | 查詢／設定 UART 鮑率（預設 115200） | 3.4 | 300 ms | 寫入後立即生效，主機端未同步改就會變亂碼並失聯；AT&F 與 ATZ 不會把它還原成預設值 |

**URC**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QINDCFG="all"` | 查詢 URC 總開關目前狀態 | LPM §3.2 / AT手冊 §4.4 | 300 ms | — |
| `AT+QINDCFG="csq",1` | 開啟訊號強度變化自動回報 | LPM §3.2 / AT手冊 §4.4 | 300 ms | 若第三參數 <savetonvram> 帶 1 則寫 NVRAM。 |
| `AT+QINDCFG="sqi",1` | 開啟 RSRP/RSRQ/SINR 變化自動回報 | LPM §3.2 / AT手冊 §4.4 | 300 ms | 若第三參數 <savetonvram> 帶 1 則寫 NVRAM；省略則僅本次開機有效。 |
| `AT+QINDCFG=?` | 查詢支援的 URC 類型與存檔選項 | LPM §3.2 / AT手冊 §4.4 | 300 ms | — |
| `AT+QURCCFG="urcport"` | 查詢目前 URC 從哪個埠輸出 | LPM §3.1 / §5.4.2 / AT手冊 §2.24 | 300 ms | — |
| `AT+QURCCFG="urcport","uart1"` | 把 URC 輸出埠切到主 UART | LPM §3.1 / §4.1.2 | 300 ms | 寫 NVRAM（AT 手冊 §2.24 Characteristics：The configuration is sav… |
| `AT+QURCCFG=?` | 查詢模組支援哪些 URC 輸出埠 | LPM §3.1 / §5.4.2 / AT手冊 §2.24 | 300 ms | — |

### Basic（19 條）

**Diagnostics**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CEER` | 回報上一次失敗操作的延伸錯誤原因文字 | 4.2 | 300 ms | — |
| `AT+QCFG=?` | 列出本機實際支援的所有 QCFG 子項與參數範圍 | 4.3 | 300 ms | — |

**Network**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CGATT` | 查詢或設定 PS（封包域）附著狀態 | 10.1 | 140 s（由網路決定） | 寫入形式 AT+CGATT=0 會脫離封包域、切斷所有資料連線（會連帶打斷 TCP/IP 與 MQTT 頁簽正在進行的測… |
| `AT+COPS=?` | 掃描並列出周邊所有可見電信業者 | 6.1 | 300 s（由網路決定） | 長時間阻塞（實測常 30–120 秒，手冊標 300 秒）；掃描期間模組會脫離現有服務，導致資料連線中斷 |
| `AT+QCFG="band"` | 設定偏好搜尋的 GSM/WCDMA/LTE 頻段 | 4.3.6 | 150 s | 寫入自動存 NVRAM；設成模組不支援的頻段會回 ERROR；鎖錯頻段會完全搜不到網 |
| `AT+QCFG="nwscanmode"` | 鎖定搜網制式（自動／GSM／WCDMA／LTE） | 4.3.2 | 150 s | 寫入自動存 NVRAM；設成模組不支援或與現行服務域衝突的制式會回 ERROR，設錯可能導致完全搜不到網 |

**PDP（建議新增組別）**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CGACT` | 啟用或停用指定的 PDP context | 10.7 | 150 s（由網路決定） | AT+CGACT=0,<cid> 會停用 PDP、切斷該 context 上的所有資料（會連帶打斷 TCP/IP 與 M… |
| `AT+CGDCONT` | 定義與查詢 PDP context（APN 設定） | 10.2 | 3 s | 寫入形式的設定會自動保存並在斷電後保留（手冊 NOTE：PDP context parameters can be sa… |
| `AT+CGEREP` | 開啟封包域事件 URC（+CGEV）回報 | 10.12 | 300 ms | — |
| `AT+CGPADDR` | 顯示各 PDP context 取得的 IP 位址 | 10.9 | 300 ms | — |
| `AT+QGDCNT` | 查詢/重設模組累計收發位元組數 | 10.15 | 300 ms | AT+QGDCNT=1 會把計數結果寫入 NVRAM（頻繁執行會磨損 flash）；AT+QGDCNT=0 會歸零計數，… |

**SIM**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QINISTAT` | 查詢 SIM 卡初始化進行到哪個階段 | 5.9 | 300 ms | — |
| `AT+QSIMSTAT` | 查詢 SIM 是否插入並開關插拔狀態 URC | 5.11 | 300 ms | 寫入形式需重開機才生效並自動存 NVRAM |

**Status**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CFUN=` | 設定射頻功能等級／軟重啟模組 | 2.21 | 15 s（依網路而定） | CFUN=0/4 會立刻脫網、斷掉所有 PDP 與 socket；CFUN=1,1 會軟重啟模組使 AT 口短暫失效；C… |
| `AT+CFUN=0 / AT+CFUN=1` | 關 RF 再開，強制重新掛網 | 1.2 | - | 斷線：關閉射頻會踢掉網路註冊、所有 PDP context 與 socket 全斷；重新註冊需數秒到數十秒 |
| `AT+CMEE` | 設定錯誤碼格式（關閉／數字／文字） | 2.22 | 300 ms | — |
| `AT+QLTS` | 取得網路同步的最新時間與時區 | 6.8 | 300 ms | — |

**URC**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QINDCFG` | 逐類開關 URC 主動上報（訊號、網路制式、簡訊等） | 4.4 | 300 ms | <savetonvram>=1 會寫入 NVRAM 使設定跨重開機保留 |
| `AT+QURCCFG` | 設定 URC 從哪個實體埠輸出 | 2.24 | 300 ms | 設定自動存檔（跨重開機生效）；設成 usbat/usbmodem 後主 UART 將完全收不到任何 URC |

### Basic（既有頁簽）（2 條）

**Network**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CGATT` | 查詢/設定 PS 網域附著狀態 | HTTP §4.2 / FTP §4.2 | 依 AT 指令手冊（本三份文件未標） | AT+CGATT=0 會中斷所有封包資料連線 |

**Status**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+CCLK` | 設定模組時間以通過憑證有效期檢查 | SSL §1.5 | 依 AT 指令手冊（本三份文件未標） | — |

### GNSS（7 條）

**AGNSS**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QAGPS=1` | 啟用 AGNSS（網路輔助定位）加速冷啟動 | 2.3.6 | 300 ms | 寫 NVRAM；須重開機才生效；會產生數據流量（下載星曆） |
| `AT+QAGPS?` | 查詢 AGNSS 功能是否已啟用 | 2.3.6 | 300 ms | — |

**GNSS Config**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QGPSCFG="outport"` | 查詢目前 NMEA 語句輸出埠 | 2.3.1.1 | 300 ms | — |
| `AT+QGPSCFG="urc",<bitmap>` | 設定 GNSS URC 回報類型 | 2.3.1.7 | 300 ms | 寫 NVRAM |

**NMEA**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QGPSCFG="gpsnmeatype",<0-127>` | 以位元遮罩設定 NMEA 輸出語句種類 | 2.3.1.3 | 300 ms | 寫 NVRAM |
| `AT+QGPSCFG="nmeasrc"` | 查詢是否允許用 AT+QGPSGNMEA 取 NMEA | 2.3.1.2 | 300 ms | — |
| `AT+QGPSGNMEA="GSA"` | 取 GSA 語句（定位模式 2D/3D 與 PDOP/HDOP/VDOP） | 2.3.5 | 300 ms | — |

### TCP-IP（16 條）

**Diagnostics**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QIDNSCFG` | 查詢或設定 PDP context 的 DNS 伺服器 | 2.3.14 | - | — |

**PDP Context**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QICSGP=1` | 查 context 1 目前的 APN 與認證設定 | 2.3.2 | - | — |

**Server**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QICFG="tcp/accept"` | 是否自動接受進來的 TCP 連線 | 2.3.1 | 300 ms | — |
| `AT+QIOPEN（"TCP LISTENER"）` | 開 TCP server 監聽指定本地埠 | 2.3.5 | 150 s | 開著會被動接受外部連線；最長阻塞 150 秒 |
| `AT+QIOPEN（"UDP SERVICE"）` | 開 UDP 服務綁定本地埠收發 | 2.3.5 | 150 s | 最長阻塞 150 秒；產生數據流量 |
| `AT+QIRD=<connectID>（不帶長度）` | 讀 UDP SERVICE 的一整包資料 | 2.3.9 | - | — |
| `AT+QISEND=<connectID>,<send_length>,"<remoteIP>",<remote_port>` | 從 UDP 服務送資料給指定遠端 | 2.3.8 | - | 進入資料模式（同定長形式）；產生數據流量 |
| `AT+QISTATE=1,<connectID>` | 查單一 socket 的狀態 | 2.3.7 | 300 ms | — |

**Socket**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QIOPEN（"UDP" client）` | 以 UDP client 連遠端主機 | 2.3.5 | 150 s | 產生數據流量 |
| `AT+QISEND=<connectID>,<send_length>（定長）` | 送固定長度資料，不需要 Ctrl+Z | 2.3.8 | - | 進入資料模式：出現 > 之後到湊滿 <send_length> 位元組之前，AT 指令無效（可用 Esc 取消） |
| `AT+QISEND=<connectID>（變長）` | 送任意文字，以 Ctrl+Z 結束 | 2.3.8 | - | 進入資料模式：出現 > 之後模組把所有輸入當資料，未送 Ctrl+Z(0x1A) 或 Esc(0x1B) 之前 AT 指… |

**Socket Config**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QICFG="TCP/SendMode"` | SEND OK 是送出即回或等 ACK 才回 | 2.3.1 | 300 ms | 設為 1–4 後 SEND OK 會延後到收到伺服器 ACK 才出現，弱網下可能等很久 |
| `AT+QICFG="dataformat"` | 設定送/收資料為文字或 Hex | 2.3.1 | 300 ms | — |
| `AT+QICFG="recvind"` | 收資料 URC 是否附帶資料長度 | 2.3.1 | 300 ms | — |
| `AT+QICFG=?` | 列出全部 socket 組態子項與值域 | 2.3.1 | 300 ms | — |

**Transparent**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `+++` | 從透傳模式逃回 AT 指令模式 | 1.3 | - | — |

### TCP/IP（既有頁簽）（1 條）

**Diagnostics**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QIDNSCFG` | 查詢/設定 PDP context 的 DNS 伺服器位址 | SSL §4 / HTTP §4.3 | 依 TCP/IP AN（本三份文件未標） | — |

### MQTT（9 條）

**Config**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QMTCFG="edit/timeout"` | 設定資料輸入逾時是否自動退出、逾時秒數（1–120） | 3.3.1 | 300 ms | — |
| `AT+QMTCFG="pdpcid"` | 指定或查詢 MQTT 走哪個 PDP context（cid 1–15，預設 1） | 3.3.1 | 300 ms | — |
| `AT+QMTCFG="recv/mode"` | 設定收到的訊息走 URC 直送或存緩衝區，及是否附長度 | 3.3.1 | 300 ms | — |
| `AT+QMTCFG="ssl"` | 開關 MQTT 的 SSL 並指定 SSL context index（0–5） | 3.3.1 | 300 ms | — |
| `AT+QMTCFG="timeout"` | 設定封包逾時秒數、重送次數、是否回報逾時 | 3.3.1 | 300 ms | 設成上限（60×10）後，後續 SUB/UNS/PUB 最長可阻塞 600 秒 |
| `AT+QMTCFG=?` | 列出本韌體支援的所有 MQTT 設定子項與參數範圍 | 3.3.1 | 300 ms | — |

**Pub / Sub**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QMTPUBEX=?` | 查發布指令的參數範本，可當場證明末參數是長度 | 3.3.8 | <pkt_timeout> × <retry_times>（預設 15 s），實務上即刻回覆 | — |

**Recv**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QMTRECV` | 把緩衝區裡的訊息讀出來（recv_id 0–4，省略則全讀） | 3.3.9 | 手冊未列（-） | — |
| `AT+QMTRECV?` | 查 5 格接收緩衝區各自有無未讀訊息 | 3.3.9 | 手冊未列（-） | — |

### SSL（新頁簽）（12 條）

**Info**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QSSLCFG=?` | 一次列出全部 SSL 組態子項與可設範圍 | SSL §2.2.1 | 300 ms | — |

**SSL Context**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QSSLCFG="ciphersuite"` | 設定/查詢加密套件 | SSL §2.2.1 | 300 ms | — |
| `AT+QSSLCFG="ignorelocaltime"` | 是否略過憑證有效期檢查 | SSL §1.5 / §2.2.1 | 300 ms | — |
| `AT+QSSLCFG="negotiatetime"` | 設定 SSL 握手最大逾時秒數 | SSL §2.2.1 | 300 ms | — |
| `AT+QSSLCFG="seclevel"` | 設定驗證模式：0 不驗 /1 驗伺服器 /2 雙向 | SSL §2.2.1 | 300 ms | — |
| `AT+QSSLCFG="sni"` | 開關 Server Name Indication | SSL §1.6 / §2.2.1 | 300 ms | — |
| `AT+QSSLCFG="sslversion"` | 設定/查詢該 SSL context 的 TLS 版本 | SSL §2.2.1 | 300 ms | — |

**TLS Socket**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QSSLCLOSE` | 關閉指定的 TLS 連線 | SSL §2.2.5 | 由 <close_timeout> 決定（預設 10 s） | 長時間阻塞：回應時間由 <close_timeout> 決定，最大可設到 65535 |
| `AT+QSSLOPEN` | 建立 TLS socket 連到遠端伺服器 | SSL §2.2.2 | 最大網路回應 150 s，再加上 <negotiate_time>（預設 300 s） | 耗流量；長時間阻塞（最壞 150 s + negotiatetime 300 s = 450 s）；access_mod… |
| `AT+QSSLRECV` | 從緩衝區讀取 TLS 收到的資料 | SSL §2.2.4 | 300 ms | — |
| `AT+QSSLSEND` | 經 TLS 連線送出資料 | SSL §2.2.3 | 300 ms | 耗流量；進入 > 提示等待狀態，未送 CTRL+Z 或 ESC 前後續 AT 指令會被當成資料 |
| `AT+QSSLSTATE` | 查詢 TLS 連線狀態 | SSL §2.2.6 | 300 ms | — |

### HTTP（新頁簽）（11 條）

**HTTP Config**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QHTTPCFG="contextid"` | 指定 HTTP 使用哪個 PDP context | HTTP §2.3.1 | 300 ms | — |
| `AT+QHTTPCFG="responseheader"` | 開關 HTTP 回應標頭輸出 | HTTP §1.3.2 / §2.3.1 | 300 ms | — |
| `AT+QHTTPCFG="rspout/auto"` | 開關 HTTP 回應自動輸出 | HTTP §2.3.1 | 300 ms | 啟用後 QHTTPREAD / QHTTPREADFILE 一律失敗 |
| `AT+QHTTPCFG="sslctxid"` | 指定 HTTPS 使用哪個 SSL context | HTTP §2.3.1 | 300 ms | — |

**HTTP Read**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QHTTPREAD` | 從 UART 讀出 HTTP 回應內容 | HTTP §2.3.7 | 由 <wait_time> 決定（預設 60 s） | 讀取形式進 data mode；回應內容可能為二進位並灌爆終端機；阻塞由 <wait_time> 決定（預設 60 s） |

**HTTP Request**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QHTTPGET` | 送出 HTTP(S) GET 請求 | HTTP §2.3.3 | 由 <rsptime> 決定（預設 60 s）；requestheader=1 時 CONNECT 須於 125 s 內出現 | 耗流量（GET 大檔在計量 SIM 上是真金白銀）；阻塞由 <rsptime> 決定（預設 60 s，可設到 65535… |
| `AT+QHTTPPOST` | 經 UART 送出 HTTP(S) POST 請求 | HTTP §2.3.5 | 由網路與 <rsptime> 決定（預設 60 s） | 耗流量；進 data mode 使 AT 口暫時失效；CONNECT 須於 125 s 內出現；阻塞由網路與 <rspt… |
| `AT+QHTTPSTOP` | 取消進行中的 HTTP 請求並斷開 session | HTTP §2.3.9 | 10 s | 會中斷進行中的傳輸 |
| `AT+QHTTPURL` | 設定要存取的 HTTP(S) 伺服器 URL | HTTP §2.3.2 | 由 <timeout> 決定（預設 60 s，範圍 1–65535） | 進入 data mode 使 AT 口暫時失效；未在 <timeout>（預設 60 s）內湊滿長度會失敗；長度算錯即 … |
| `AT+QHTTPURL?` | 讀回目前設定的 URL | HTTP §2.3.2 | 300 ms | — |

**Info**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QHTTPCFG?` | 一次讀回全部 HTTP 目前組態 | HTTP §2.3.1 | 300 ms | — |

### FTP（新頁簽）（16 條）

**FTP Config**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QFTPCFG="account"` | 設定 FTP 登入帳號與密碼 | FTP §2.1 | 300 ms | 查詢形式會把 FTP 密碼明文輸出到終端機 |
| `AT+QFTPCFG="contextid"` | 指定 FTP 使用哪個 PDP context | FTP §2.1 | 300 ms | — |
| `AT+QFTPCFG="filetype"` | 設定傳輸型態：0=Binary、1=ASCII | FTP §2.1 | 300 ms | 設 ASCII 傳二進位檔會靜默損毀內容且不報錯 |
| `AT+QFTPCFG="rsptimeout"` | 設定 FTP 指令回應逾時秒數 | FTP §2.1 | 300 ms | — |
| `AT+QFTPCFG="sslctxid"` | 指定 FTPS 使用哪個 SSL context | FTP §2.1 | 300 ms | — |
| `AT+QFTPCFG="ssltype"` | 選擇 FTP / FTPS 隱式 / FTPS 顯式 | FTP §2.1 | 300 ms | — |
| `AT+QFTPCFG="transmode"` | 設定主動/被動傳輸模式 | FTP §2.1 | 300 ms | — |

**FTP Directory**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QFTPCWD` | 切換伺服器上的目前工作目錄 | FTP §2.3 | 由 <rsptimeout> 決定（預設 90 s） | — |
| `AT+QFTPLIST` | 列出伺服器目錄內容 | FTP §2.11 | 由 <rsptimeout> 決定（預設 90 s） | 耗流量（少量）；<local_name>="COM:" 時進 data mode |
| `AT+QFTPPWD` | 查詢伺服器上的目前工作目錄 | FTP §2.4 | 由 <rsptimeout> 決定（預設 90 s） | — |

**FTP File**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QFTPGET` | 從伺服器下載檔案 | FTP §2.6 | 由 <rsptimeout> 決定（預設 90 s，此時語意為兩個封包之間的最大間隔） | 耗流量（下載大檔在計量 SIM 上是實際費用）；<local_name>="COM:" 時進 data mode 且內容… |
| `AT+QFTPSIZE` | 查詢伺服器上某檔案的大小 | FTP §2.7 | 由 <rsptimeout> 決定（預設 90 s） | — |

**FTP Session**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QFTPCLOSE` | 登出 FTP(S) 伺服器 | FTP §2.18 | 由 AT+QFTPCFG="rsptimeout" 的 <timeout> 決定（預設 90 s） | — |
| `AT+QFTPOPEN` | 登入 FTP(S) 伺服器 | FTP §2.2 | 125 s | 耗流量；固定阻塞上限 125 s |
| `AT+QFTPSTAT` | 查詢 FTP 伺服器連線狀態 | FTP §2.17 | 由 <rsptimeout> 決定（預設 90 s） | — |

**Info**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `AT+QFTPCFG=?` | 列出全部 FTP 組態子項與範圍 | FTP §2.1 | 300 ms | — |

### 固定區（頁簽外，全域可見）（1 條）

**Data Mode**

| 指令 | 用途 | 章節 | 逾時 | 風險 |
|---|---|---|---|---|
| `+++` | 從資料模式脫離、回到 AT 指令模式 | SSL §1.4 / HTTP §1.4 / FTP §1.5 | 手冊未標；成功時回 OK | — |

## §4 可選（延後處理）

共 138 條。以下只列**建議頁簽非「不收錄」**者，其餘多為同一指令的其他參數形式。

| 指令 | 用途 | 建議頁簽 | 為何列為可選 |
|---|---|---|---|
| `AT+CLCK` | 鎖定／解鎖／查詢 SIM 卡與網路的各項鎖 | Basic | AT+CLCK="SC",2 查詢 PIN 鎖狀態（0=關、1=開）是唯讀且實用的——工具現在只能靠 AT+CPIN? 回 READY 間接推測，看不出「PIN 鎖其實是開的只是已… |
| `AT+CNUM` | 讀取 SIM 卡本機門號 MSISDN | Basic | 整個第 8 章唯一有實用價值的一條：唯讀、300 ms、無副作用，可回答「這張測試卡的門號是多少」。但現實上絕大多數 M2M / IoT SIM 的 EF-MSISDN 是空的，回… |
| `AT+CPAS` | 查詢行動裝置活動狀態（就緒／響鈴／通話中） | Basic | <pas> 值 0=Ready、2=Unknown、3=Ringing、4/6=通話中或保留，語意幾乎全繞著語音通話轉。本工具不做語音，唯一剩下的價值是拿 +CPAS: 0 當「模… |
| `AT+CPOL` | 讀取與編輯 SIM 偏好業者清單 | Basic | 只有 Read form（AT+CPOL?）值得考慮：可解釋「為什麼模組偏偏選了某家業者 / 為什麼漫遊時跳到奇怪的網」。寫入形式改的是 SIM 卡本身、不是模組設定，改壞了換張卡… |
| `AT+CPWD` | 變更 SIM 或通話限制功能的密碼 | Basic | 驗證「改密碼→重開機→用新密碼解鎖」的完整流程時會用到，但這是低頻操作，而且在一個按鈕式 UI 上誤觸的代價很高（測試 SIM 的 PIN 被改掉，下次別人拿去用就解不開）。AT+… |
| `AT+CRSM` | 受限存取 SIM 檔案（讀寫 EF 基本檔） | Basic | 進階除錯有價值：<command>=176（READ BINARY）、178（READ RECORD）、192（GET RESPONSE）、242（STATUS）四種是唯讀且安全的… |
| `AT+CSCS` | 選擇 TE 字元集（GSM／IRA／UCS2） | Basic | 手冊 1.5 說明字元集只影響簡訊、CBS 與電話簿文字欄位的收送與顯示。本工具不做 SMS、不做電話簿，實用性低。唯一有點價值的是唯讀的 AT+CSCS?（確認目前是 GSM），… |
| `AT+CTZR` | 開關時區變更事件的 URC 回報 | Basic | 時區變更是極低頻事件（跨國移動或網路調整才會觸發），一個手動下指令做功能驗證的場景幾乎不可能等到 +CTZV / +CTZE。與 AT+CTZU 一樣需重開機才生效。價值明顯低於同… |
| `AT+CTZU` | 查詢/開關 NITZ 自動時區更新 | Basic | 只有 AT+CTZU? 值得補，用來解釋「為什麼 AT+CCLK? 的時間是錯的」——若 <onoff>=0 就是沒開 NITZ。寫入形式的陷阱很大：手冊 Characterist… |
| `AT+QCFG="gprsattach"` | 設定開機時 GPRS 自動或手動附著 | Basic | 0=手動附著、1=自動附著。手冊 NOTE 1 警告此設定會連帶影響模組支援的網路模式。要重開機才生效，加上 150 秒的回應上限，對「下指令馬上看結果」的手動驗證流程很不友善。查… |
| `AT+QCFG="nwscanseq"` | 設定搜網制式的優先順序 | Basic | 13 個值（0–12）涵蓋各種制式排列組合。對 LTE 為主的 EG800K，調搜網順序的實用性遠低於 nwscanmode 直接鎖制式，加上要重開機、150 秒逾時、手冊自身敘述… |
| `AT+QCFG="servicedomain"` | 設定註冊服務域（CS／PS／CS&PS） | Basic | <service> 0=CS only、1=PS only、2=CS&PS；<effect> 0=重開機生效（手冊註明目前不支援）、1=立即生效。對純數據驗證，正確答案永遠是 2 … |
| `AT+QCFG="urc/cache"` | 開關 URC 快取功能 | Basic | 手冊範例把它示範得很清楚：開啟期間打進來的 RING、NO CARRIER、+CMTI 全被壓住，一關掉才一次全吐出來。對即時終端機觀察百害無一利。但查詢形式（確認它是 0）有價值… |
| `AT+QSIMDET` | 開關 SIM 卡熱插拔偵測並設定插入時的腳位電位 | Basic | 驗證客戶板上 SIM 座偵測腳的必備指令：<enable> 0/1，<insert_level> 0=插入時低電位／1=插入時高電位。設定正確後拔卡會看到 +CPIN: NOT R… |
| `+++` | 從資料模式切回 AT 命令模式 | Basic（需終端機支援裸位元組送出後再評估） | 是模組誤入資料模式時的唯一軟體救援手段（另一條路是靠 DTR 準位，見 AT&D §3.2）。但實作前必須先確認本工具的終端機能否送出「不帶行尾字元」的裸 +++ 並滿足前後各 1… |
| `AT+QFTPCFG="data_address"` | 決定資料連線要用哪個位址 | FTP（新頁簽） | 看起來冷門但治一個典型故障：passive mode 下伺服器若回報自己的私有 IP（NAT 後面的 FTP server 常見），模組會連不上資料通道，控制通道卻是通的，症狀是 … |
| `AT+QFTPDEL` | 刪除伺服器上的檔案 | FTP（新頁簽） | 這三份文件裡破壞力最強的一條——不可復原，而且刪的是**遠端伺服器**上別人的資料，不是模組自己的。功能上確實屬於完整 FTP 驗證的一環（手冊 §1.4 也把它列進標準流程），所… |
| `AT+QFTPLEN` | 查詢已傳輸的資料長度 | FTP（新頁簽） | 執行式無參數，回 +QFTPLEN: 0,<transferlen>，用來在 QFTPPUT/QFTPGET/QFTPLIST/QFTPNLST 之後確認實際搬了多少 byte。當… |
| `AT+QFTPMDTM` | 查詢檔案的最後修改時間 | FTP（新頁簽） | 回 +QFTPMDTM: 0,"YYYYMMDDHHMMSS"。不進 data mode、零風險，但 QFTPLIST 的輸出通常已經含時間，資訊重複。要做 OTA 版本比對時才有… |
| `AT+QFTPMKDIR` | 在伺服器上建立資料夾 | FTP（新頁簽） | 寫入類操作，動的是遠端伺服器。做「完整 CRUD 驗證」時需要，一般連線驗證用不到。與 RMDIR/RENAME/DEL 應該一起放進需要展開的 Danger 分組，避免誤按。 |
| `AT+QFTPMLSD` | 列出標準化的檔案與目錄資訊 | FTP（新頁簽） | MLSD 是 RFC3659 的機器可讀列表格式，欄位固定、比 LIST 好解析。問題是不少舊 FTP 伺服器根本沒實作，會回 protocol_error=500/502（com… |
| `AT+QFTPNLST` | 只列出目錄下的檔名 | FTP（新頁簽） | QFTPLIST 的精簡版，只回檔名、沒有大小與時間。輸出短、比較不會灌爆終端機是唯一優勢，但資訊量明顯不足，功能與 QFTPLIST 重疊。兩者只做一個的話選 QFTPLIST。 |
| `AT+QFTPPUT` | 上傳檔案到伺服器 | FTP（新頁簽） | 三條路都不輕鬆："COM:" 要進 data mode 手動餵位元組、以 +++ 結束（手冊 §1.5 明講 QFTPPUT 之後**不能**用 ATO 回到 data mode，… |
| `AT+QFTPRENAME` | 重新命名伺服器上的檔案或資料夾 | FTP（新頁簽） | 同時適用檔案與目錄。破壞力比 DEL/RMDIR 小（可以改回來），但仍是改動遠端資料。歸在 Danger 分組。 |
| `AT+QFTPRMDIR` | 刪除伺服器上的資料夾 | FTP（新頁簽） | 同 QFTPDEL，不可復原且作用在遠端。整個目錄一次消失，破壞面比刪單檔更大。Danger 分組加二次確認。 |
| `AT+QAGPS=0` | 停用 AGNSS 功能 | GNSS | 做「有 AGNSS vs 無 AGNSS」的 TTFF 對照實驗時需要，補的話應與 =1 成對。單獨存在意義不大。 |
| `AT+QAGPS=?` | 測試 AGNSS 功能是否存在 | GNSS | 回傳僅 (0,1)，資訊量低，但可快速確認韌體有無帶 AGNSS。優先度低於讀取版。 |
| `AT+QAGPSCFG=?` | 列出 AGNSS 參數的支援範圍 | GNSS | 純查詢。手冊註明只有部分機型支援本指令，實測可能直接回 ERROR，這本身也算一種資訊。優先度低。 |
| `AT+QAGPSCFG?` | 查詢 AGNSS 伺服器位址與帳密設定 | GNSS | 純查詢。AGNSS 下載失敗（+QGPS: "agps" 回 5 或 6）時，確認伺服器位址是否被改壞的唯一途徑。手冊也建議動任何 AGNSS 參數前先用它抄下預設值。但屬低頻除錯… |
| `AT+QGPS=?` | 測試 GNSS 功能是否存在並列出支援狀態值 | GNSS | 回傳內容幾乎沒有資訊（就 (0,1)），但若模組是無 GNSS 選配版本會直接回 ERROR——這是三秒內判斷「這顆料到底有沒有 GNSS」最快的方法。EG800K 系列 GNSS… |
| `AT+QGPSCFG="apflash"` | 查詢 AP-Flash 快速熱啟動是否啟用 | GNSS | 純查詢。做 TTFF（首次定位時間）對比測試時有用，一般功能驗證用不到。 |
| `AT+QGPSCFG="apflash",<0\|1>` | 啟用/停用 AP-Flash 快速熱啟動 | GNSS | 星曆存本地 flash、有效 1 小時、每小時自動更新。手冊 §4.3 註明它與備援電源功能互斥，須先 AT+QGPSVBCKP=0；但 EG800K-CN 硬體本就不支援備援電源… |
| `AT+QGPSCFG="autogps"` | 查詢開機是否自動啟動 GNSS | GNSS | 純查詢無害。對「為什麼一開機 GNSS 就在跑 / 就是不跑」有解釋力，但不是日常驗證的高頻指令。 |
| `AT+QGPSCFG="autogps",<0\|1>` | 設定開機自動啟動 GNSS | GNSS | 手冊 Characteristics 明寫「重開機後才生效」。工程師手動下完看不到任何變化會誤判失敗，UI 必須標「需重開機」。屬產品部署設定而非功能驗證，優先度低。 |
| `AT+QGPSCFG="nmeasrc",0` | 停用經 AT 口取得 NMEA | GNSS | 只有在刻意驗證 507 錯誤行為時才需要。補的話務必與 nmeasrc,1 成對放，避免工程師設了 0 之後忘記還原。 |
| `AT+QGPSCFG="ntp"` | 查詢 GNSS 專用 NTP 伺服器位址 | GNSS | 純查詢。手冊註明 EC200A-CN/EC200A-CNV1/EG950A 不支援，EG800K 不在排除名單內故應可用。查得到原廠預設位址，在懷疑時間注入失敗拖慢 TTFF 時有… |
| `AT+QGPSCFG="outport","none"` | 關閉 NMEA 語句輸出埠 | GNSS | 設下去會斷電保留，之後換人接手會以為模組壞了。對測試工具的價值低，但列出來讓工程師知道「別人可能把它設成 none」有診斷意義。 |
| `AT+QGPSCFG="outport","uartdebug"` | 把 NMEA 語句導向 debug UART 埠 | GNSS | 關鍵陷阱：uartdebug 是 debug UART，不是本工具連的主 UART AT 口。工程師很容易誤以為設了這個就能在終端機看到 NMEA。要補就必須在 UI 上標注這點，… |
| `AT+QGPSCFG="outport","usbnmea"` | 把 NMEA 語句導向 USB NMEA 埠（原廠預設） | GNSS | 本工具走串列 AT 口、不掛 USB 網卡，導到 USB NMEA 埠在終端機上看不到任何東西。價值僅止於「把別人改壞的設定改回預設」。 |
| `AT+QGPSGNMEA="GLL"` | 取 GLL 語句（經緯度與 UTC 時間） | GNSS | 內容是 GGA/RMC 的子集，沒有獨有欄位。補齊 7 種語句求完整可以，功能驗證上沒有非它不可的理由。 |
| `AT+QGPSGNMEA="GST"` | 取 GST 語句（虛擬距離誤差統計） | GNSS | 提供緯度/經度/高度的標準差估計，做定位精度量化評估時有用。但手冊兩處註明「部分機型不支援 GST」，EG800K 是否支援需實測；若不支援會回錯誤，UI 要能友善呈現而非看起來像… |
| `AT+QGPSGNMEA="VTG"` | 取 VTG 語句（對地航向與地面速度） | GNSS | 航向與速度資訊在 RMC 裡已經有一份，且靜態桌面測試時速度恆為 0、航向為空。只有做車載移動測試才需要。 |
| `AT+QGPSGNMEA=?` | 列出本機型支援的 NMEA 語句類型 | GNSS | 純查詢。手冊註明「部分機型不支援 GST」，這條可實測確認 EG800K 到底吃不吃 GST，省掉問原廠的時間。 |
| `AT+QGPSLOC=1` | 取定位資訊（度分格式，分位到小數 6 位，經緯與方位分欄） | GNSS | 介於 mode 0 與 2 之間的第三種格式，精度比 mode 0 高兩位。工具已有 0 與 2 涵蓋「原始格式」與「十進位可直接貼地圖」兩大需求，mode 1 屬錦上添花。 |
| `AT+QGPSVBCKP=0` | 宣告未接 GNSS 備援電源（啟用 AP-Flash 的前置） | GNSS | 手冊 §4.3 明講：備援電源預設自動啟用，要用 AP-Flash 熱啟動必須先下這條關掉。只有在做 AP-Flash 熱啟動測試時才成對使用；EG800K-CN 既然硬體不支援備… |
| `AT+QGPSVBCKP=?` | 測試 GNSS 備援電源功能是否支援 | GNSS | 對 EG800K-CN 而言，這條的主要價值是驗證手冊說法——回 ERROR 即坐實本機型不支援備援電源。一次性確認用，不需常駐 UI。 |
| `AT+QGPSVBCKP?` | 查詢是否已宣告接上 GNSS 備援電源腳位 | GNSS | 純查詢。手冊 §4.3 說備援電源預設自動啟用、且與 AP-Flash 互斥，要用 AP-Flash 前得先確認這個值。但 EG800K-CN 硬體不支援備援電源，實用性存疑。 |
| `AT+QHTTPCFG="closed/ind"` | 開關 HTTP session 關閉的 URC 通知 | HTTP（新頁簽） | 啟用後 session 關閉時會回報 +QHTTPURC: "closed"。對長時間掛著觀察連線生命週期有幫助，屬「知道比不知道好」但非必要。成本極低，若 HTTP 頁還有空位可… |
| `AT+QHTTPCFG="contenttype"` | 設定 POST body 的 Content-Type | HTTP（新頁簽） | 只在 POST 時有意義，六選一：0=x-www-form-urlencoded、1=text/plain、2=octet-stream、3=multipart/form-data… |
| `AT+QHTTPCFG="reqheader/add"` | 加入自訂 HTTP 請求標頭 | HTTP（新頁簽） | 比 requestheader=1 溫和得多的做法：只加一兩個 header（例如 Authorization: Bearer xxx），其餘仍由模組自動填。對測需要 token … |
| `AT+QHTTPCFG="reqheader/remove"` | 移除先前加入的自訂請求標頭 | HTTP（新頁簽） | reqheader/add 的配套，成對出現才完整；單獨做沒意義。因為組態不進 NVRAM、重開機自動清空，緊急時直接重開機也能達到同樣效果，所以優先度低於 add。 |
| `AT+QHTTPCFG="requestheader"` | 開關「自行輸入完整請求標頭」模式 | HTTP（新頁簽） | 設 1 之後 AT+QHTTPGET 與 AT+QHTTPPOST 的語法都會改變（GET 從 AT+QHTTPGET=<rsptime> 變成必須帶 <data_length> … |
| `AT+QHTTPCFG=?` | 列出全部 HTTP 組態子項與範圍 | HTTP（新頁簽） | 與 AT+QHTTPCFG?（讀取式）功能重疊，而後者直接吐出「目前實際值」比吐「可設範圍」有用。兩者只需擇一，建議做讀取式那條。 |
| `AT+QHTTPGETEX` | 指定位移與長度的分段 GET | HTTP（新頁簽） | AT+QHTTPGETEX=<rsptime>,<start_position>,<read_len>，伺服器會以 206 回應。測 OTA 韌體分段下載時很實用，可避免一次抓進 … |
| `AT+QHTTPPOSTFILE` | 以 UFS 檔案內容送出 POST 請求 | HTTP（新頁簽） | 要先用 AT+QFUPL 把檔案塞進模組才有東西可 POST，對純 UART 手動測試是繞遠路。<post_mode> 還支援 0/1/2 的兩檔合併送出。除非要測固定 paylo… |
| `AT+QHTTPREADFILE` | 把 HTTP 回應直接存成 UFS 檔 | HTTP（新頁簽） | 對抓大檔比 AT+QHTTPREAD 好用得多：不進 data mode、不會把幾百 KB 的內容灌進瀏覽器終端機，只回一行 +QHTTPREADFILE: <err>。代價是要再… |
| `AT&W` | 把目前 AT 設定存入使用者 profile（非揮發記憶體） | Hardware | 只有 AT&W[0] 一個 profile。單獨使用沒意義，實際價值在於搭配 AT+IPR / AT+IFC 改完後存檔（手冊 3.4 範例即 AT+IPR=115200;&W）。… |
| `AT+QCFG="airplanecontrol"` | 開關由 W_DISABLE# 腳控制飛航模式 | Hardware | 硬體驗證有價值：啟用後拉低 W_DISABLE#，可觀察到 +QIND: airplanestatus,1 並且 AT+CFUN? 變 4，拉高則回 1，能一次驗證腳位走線與韌體行… |
| `AT+QCFG="risignaltype"` | 設定 RI 訊號輸出載體（實體腳或虛擬） | Hardware | "respective"=RI 跟著 URC 所在的埠走（URC 在 USB 埠就是虛擬 RI，該埠不支援 RI 就完全沒有）、"physical"=不管 URC 在哪個埠都只驅動… |
| `AT+QCFG="urc/ri/other"` | 設定一般 URC 出現時 RI 腳的脈波行為 | Hardware | <typeRI> "off"=RI 不動作、"pulse"=送脈波；<pulse_duration> 5–2000 ms（預設 120）、<pulse_count> 1–5（預設 … |
| `AT+QINDCFG="act",1` | 開啟接入技術變化自動回報 | Hardware | 回報 +QIND: "act","LTE"/"HSDPA"/"EGPRS"…。手冊註明開啟當下就會立即報一次，之後僅在制式變更時報。功能與現有 AT+QNWINFO 重疊，但 QN… |
| `AT+QINDCFG="all",0` | 關閉全部 URC 回報（進睡眠前用） | Hardware | LPM §3.2 的正規用法：主機睡前關掉不需要的 URC，避免 MAIN_RI 頻繁把主機叫醒。對本工具的次要價值是「終端機被 URC 洗版時一鍵靜音」。但要警告使用者這會讓 M… |
| `AT+QPOWD` | 軟體關機，模組去註冊網路後進入 shutdown | Hardware | 對驗證關機序列（POWERED DOWN URC、STATUS pin 拉低時序、去註冊耗時）的工程師有價值，但按下去整顆模組就沒了，必須靠 PWRKEY 或重新上電才能救回，串列… |
| `AT+QPOWD` | 軟關機（關機後 12 秒才可斷電） | Hardware | 流程圖列為建議的關機程序（送 QPOWD → 等 12 秒以上 → 切電）。放進工具能驗完整關機流程，但按下去就再也下不了指令，而串列測試治具通常沒有 PWRKEY 控制線。要收就… |
| `AT+QRFTESTMODE=?` | 查詢模組是否支援出廠測試模式 | Hardware | 唯一有獨立價值的 FTM 指令：這是**確認本機是否支援 FTM 的唯一文件內方法**。FTM 手冊 §1 NOTE 明寫「2 MB Flash 機型不支援 FTM」與「EG800… |
| `AT+QRFTESTMODE?` | 查詢模組目前是否處於出廠測試模式 | Hardware | 唯讀、零風險，可用來確認模組沒有卡在 FTM。實務價值在於：若同事或前一輪測試把模組留在 FTM=1，模組不會入網，這條能一秒看出來（配 AT+QRFTESTMODE=0 脫困）。… |
| `AT+QSCLK` | 開關睡眠模式，由 DTR 與 WAKEUP_IN 腳控制 | Hardware | 低功耗驗證會用到，但這是本章唯一會讓 AT 口「當場失聯」的指令。手冊寫明：<n>=1 時若 DTR 腳與 WAKEUP_IN 腳皆被拉高，模組直接進入睡眠；若兩腳皆為低，則需先把… |
| `AT+QSCLK=1` | 允許模組進入睡眠（仍受 DTR 閘控） | Hardware | 低功耗驗證的核心指令，但對本工具是雙面刃。AT 手冊 §11.3 明寫：致能後若 DTR 與 WAKEUP_IN 皆為高電位，模組會「直接進入睡眠」；LPM 表 2 也寫 MAIN… |
| `AT+QSCLK=?` | 查詢模組支援哪些睡眠致能參數 | Hardware | 只回傳 (0,1)，資訊量低；但可用來確認韌體是否實作睡眠控制。與 AT+QSCLK? 二擇一即可。 |
| `ATZ` | 重設為出廠值後再套用使用者 profile | Hardware | 功能等於 AT&F 再疊上 AT&W 存過的 profile。若使用者從沒下過 AT&W，效果與 AT&F 幾乎相同，優先度低於 AT&F。工具若同時放 AT&F 與 ATZ，要在… |
| `AT+QMTCFG="close/time"` | 設定心跳逾時後回報 +QMTCLOSE 的最大間隔（5–60 秒） | MQTT | 只影響「斷線多久後才回報」的時機，功能驗證用不到。而且它是全部 QMTCFG 子項裡唯一沒有 <client_idx> 的（語法 AT+QMTCFG="close/time"[,<… |
| `AT+QMTCFG="dataformat"` | 同時設定送出與接收方向的資料格式（String / Hex） | MQTT | 比 "send/mode" 多管接收方向，收二進位 payload（例如 protobuf）時比較實用，因為 String 模式下不可列印位元組會在終端機炸成亂碼。缺點是與 "se… |
| `AT+QMTCFG="protocol/check"` | 開關 MQTT 協定合規檢查（0=關、1=開） | MQTT | 手冊只給 0/1 兩個值，既沒說檢查什麼、也沒用底線標出預設值，實用價值不明。排查怪異 broker 相容性問題時可當備用開關，但不該放在主要按鈕列。注意其查詢回應格式與其他子項不… |
| `AT+QMTCFG="send/mode"` | 設定發布內容格式：0=String、1=Hex | MQTT | 要發二進位 payload 時有用（角色相當於 TCP/IP 頁的 QISENDEX hex）。但要說清楚：它不會讓 QMTPUBEX 變成單行指令，仍然要進 > 資料模式，只是把… |
| `AT+QMTCFG="session"` | 設定 clean session（0=伺服器保留訂閱、1=清空重來） | MQTT | 只有在驗證「斷線後 QoS1 離線訊息是否補送」這種情境才用得到，而且手冊 NOTE 2 註明 <clean_session>=0 僅在 broker 本身支援 session 儲… |
| `AT+QMTCFG="wakeup/topic"` | 指定收到特定 topic 時喚醒主機並回報 | MQTT | V1.5 新增，給低功耗喚醒情境用；手冊註明要先訂閱該 topic 才會生效，且 <wakeup_topic_enable>=0 又省略 <topic_string> 時會清掉所有… |
| `AT+QMTCFG="will"` | 設定遺囑訊息的 flag / QoS / retain / topic / 內容 | MQTT | 驗證「模組被拔電後 broker 是否發出遺囑」時有用，而且與下一條 willex 不同，它是單行指令、不需要資料模式，本工具送得出去。手冊 NOTE 1：<will_fg>=1 … |
| `AT+QMTCLOSE=?` | 查支援的 client_idx 範圍 | MQTT | 只回 (0-5)，資訊量極低，僅適合併入能力探測按鈕。 |
| `AT+QMTCONN=?` | 查連線指令的參數範本 | MQTT | 回 +QMTCONN: (0-5),"clientid","username","password"，可用來提醒使用者帳密參數的位置與順序，但資訊量仍低，適合併入能力探測。 |
| `AT+QMTDISC=?` | 查支援的 client_idx 範圍 | MQTT | 只回 (0-5)，同上，資訊量低，僅適合併入能力探測按鈕。 |
| `AT+QMTOPEN=?` | 查 client_idx 與 port 的合法範圍 | MQTT | 只回固定的 +QMTOPEN: (0-5),"hostname",(1-65535)，資訊量低，主要價值是確認這顆韌體有沒有編進 MQTT 功能。可與其他 test 指令合併成一顆… |
| `AT+QMTSUB=?` | 查訂閱指令的參數範本 | MQTT | 回 +QMTSUB: (0-5),<msgid>,list of ["topic",qos]，可提醒可一次訂閱多組 topic/qos。資訊量中低，適合併入能力探測。 |
| `AT+QMTUNS=?` | 查取消訂閱指令的參數範本 | MQTT | 回 +QMTUNS: (0-5),<msgid>,list of ["topic"]。資訊量低，適合併入能力探測。 |
| `AT+QSSLCFG="alpn"` | 設定 ALPN 協定名稱 | SSL（新頁簽） | 看似冷門但有一個明確用途：某些雲端 IoT 平台要求以 ALPN 在 443 埠上跑 MQTT。工具若日後要測 MQTT over TLS 就會需要它，屬「知道它存在、放在進階區」… |
| `AT+QSSLCFG="cacert"` | 指定信任 CA 憑證在 UFS 的路徑 | SSL（新頁簽） | 只有 seclevel≥1 才會用到，且路徑指向的檔案必須先用 AT+QFUPL（FILE AN，本三份文件之外）串進模組 UFS。在瀏覽器工具裡要送 binary 憑證檔進 da… |
| `AT+QSSLCFG="cacertex"` | 一次查/設全部 6 個 context 的 CA 路徑 | SSL（新頁簽） | cacert 的批次版：全部參數省略時會一口氣列出 context 0–5 的 CA 路徑。當診斷鈕（「我到底在哪個 context 設過憑證」）滿好用，但功能與 cacert 重… |
| `AT+QSSLCFG="clientcert"` | 指定用戶端憑證路徑（雙向驗證用） | SSL（新頁簽） | 只有 seclevel=2 且伺服器要求 client cert 時才需要，屬進階情境。與 cacert 同樣卡在 AT+QFUPL 這一關。查詢形式（省略路徑）成本低，可先做。 |
| `AT+QSSLCFG="clientkey"` | 指定用戶端私鑰路徑與密碼 | SSL（新頁簽） | 與 clientcert 成對使用，多一個 <key_pwd> 參數。同樣依賴 AT+QFUPL。注意查詢形式會把私鑰密碼原文吐回終端機，工具若有日誌功能要考慮遮蔽。 |
| `AT+QSSLCFG="ignoreinvalidcertsign"` | 是否略過無效憑證簽章 | SSL（新頁簽） | 同上，用來二分法定位握手失敗是不是簽章驗證造成的。與 ignoremulticertchainverify、ignorelocaltime 三個是同一組「把驗證逐項關掉找兇手」的工… |
| `AT+QSSLCFG="ignoremulticertchainverify"` | 是否略過多層憑證鏈驗證 | SSL（新頁簽） | 純除錯旋鈕。當伺服器送的是中間 CA 鏈而模組只裝了 root，握手會失敗；設 1 可判定問題是不是出在鏈驗證。不是最小流程的一部分，但排錯時很省時間，建議放進「Troublesh… |
| `AT+QSSLCFG="psk"` | 設定 PSK identity 與 key | SSL（新頁簽） | 預共享金鑰 TLS，用在不想部署憑證的封閉 IoT 場景。手冊只給參數定義（identity/key 各 0–255 字元），沒有端到端範例。若使用者沒有 PSK 伺服器可測就是死… |
| `AT+QSSLCFG="session_cache"` | 開關 TLS session 續用（resumption） | SSL（新頁簽） | 效能選項，影響重連時的握手時間，對功能驗證沒有幫助。真要量測「首次握手 vs 續用握手」的耗時差異時才有意義。優先度低。 |
| `AT+QFDEL` | 刪除模組 UFS/SD 內的檔案 | SSL（新頁簽）或未來 File 頁 | 屬 FILE AN。手冊 §1.4 明講「上傳到 FTP 伺服器成功後，用 AT+QFDEL 把本地檔案刪掉」。模組 UFS 空間很小，反覆測試下載必然塞滿，沒有這條就只能重開機或… |
| `AT+QFLST` | 列出模組 UFS/SD 內的檔案 | SSL（新頁簽）或未來 File 頁 | 屬 FILE AN。手冊範例在 QFUPL 之後、QFTPGET 存檔之後都用它確認檔案存在與大小。零風險、不進 data mode，是 QFUPL / QHTTPREADFILE… |
| `AT+QFREAD` | 讀出模組 UFS/SD 內的檔案內容 | SSL（新頁簽）或未來 File 頁 | 屬 FILE AN。凡是把結果存到 UFS 的路徑（QHTTPREADFILE、QFTPGET 存檔、QFTPLIST 存檔）都要靠它才看得到內容，否則等於資料進了黑盒子。與 QF… |
| `AT+QFUPL` | 把檔案（憑證/POST body）上傳到模組 UFS | SSL（新頁簽）或未來 File 頁 | 屬 FILE AN，但三份文件都依賴它：SSL 的 cacert/clientcert/clientkey 路徑、HTTP 的 QHTTPPOSTFILE、FTP 的 QFTPPU… |
| `AT&D1` | 設 DTR 由低轉高即退出透傳 | TCP-IP | 透傳的第二條逃生路線，但前提是 UART 實體真的接了 DTR 線、而且必須在進透傳「之前」就設好。Web Serial 可以控制 DTR，所以技術上可行，但硬體沒接就完全無效。收… |
| `AT+QICFG="close/mode"` | TCP 是否採非同步斷線 | TCP-IP | 啟用後 AT+QICLOSE 會立刻回 OK 而不等對端 FIN ACK，可避開最長 10 秒的阻塞。對自動化腳本有價值；手動操作時等 10 秒無所謂。若日後做「一鍵跑完整流程」的… |
| `AT+QICFG="passiveclosed"` | 伺服器關閉時是否被動關閉 TCP | TCP-IP | 影響對端主動關線時模組要不要跟著關。屬於連線行為的細部測試；手冊沒標預設值（無底線標示），要用得先查。一般功能驗證用不到。 |
| `AT+QICFG="pdp/retry"` | PDP 啟用/停用的重試次數與時間 | TCP-IP | <counts> 2–4（實際次數 = counts+1，預設 4）、可分別對 4G / 2G 模式設定、可設單次最長時間。訊號差時 AT+QIACT 老是失敗，調它可以縮短或延長… |
| `AT+QICFG="qisend/timeout"` | 出現 > 之後等待資料輸入的逾時 | TCP-IP | 範圍 0–120 秒。工具若實作 AT+QISEND 的資料模式，這條決定使用者在對話框慢慢打字會不會被模組逾時踢掉 —— 屬於實作時要查一次、可能要設一個合理值的參數。做成使用者… |
| `AT+QICFG="send/auto"` | 週期自動送出心跳封包 | TCP-IP | <cycle_time> 20–86400 秒、<try_times> 0–10、內容可用 Hex ASCII / Hex 字串 / 純字串三種格式。做保活測試時好用，但對一般驗證… |
| `AT+QICFG="send/buffersize"` | 單次傳輸資料的最大長度 | TCP-IP | 範圍 1460–10240 byte。注意這跟 AT+QISEND 的 <send_length> 上限 1460 是兩回事，後者是每次指令的硬上限。調大只有在做大量連續送出的壓力… |
| `AT+QICFG="sendinfo"` | QISEND/QISENDEX 改以 URC 回報結果 | TCP-IP | 設 1 之後回應從 SEND OK 變成 +QISEND: <connectID>,<status>,<Freesize>，多給了目前緩衝區剩餘空間（0–10240 byte）。診… |
| `AT+QICFG="tcp/keepalive"` | TCP keep-alive 開關與探測參數 | TCP-IP | <idle_time> 1–1800 秒、<interval_time> 25–100 秒、<probe_cnt> 3–10 次。這是「連線放著一陣子就莫名斷掉」（電信商 NAT … |
| `AT+QICFG="tcp/retranscfg"` | TCP 重傳次數與重傳間隔 | TCP-IP | <retran_times> 3–12 次、<retran_time> 5–1000 ms。弱訊號環境下的重傳行為調校，屬進階參數。手動功能驗證（連得上、送得出、收得到）完全用不到… |
| `AT+QICFG="transpktsize"` | 透傳模式單包最大長度 | TCP-IP | 範圍 1–1460，預設 1024 byte。只在透傳模式下生效。工具沒做透傳之前完全用不到；未來做了透傳，它和 transwaittm 是一對，要一起收才有意義。 |
| `AT+QICFG="transwaittm"` | 透傳湊不滿一包時的等待時間 | TCP-IP | 範圍 0–20，單位 100 ms，預設 2（即 200 ms）。同 transpktsize，只有透傳模式才有意義。調小可降低小封包延遲，是透傳調校的主要旋鈕之一。 |
| `AT+QICFG="udp/readmode"` | UDP 讀取採 block 或 stream 模式 | TCP-IP | 0 = 停用 block 模式、1 = 啟用 stream 模式。只有做 UDP（尤其 UDP SERVICE）才有意義：block 模式一次讀一整包、stream 模式當串流讀。… |
| `AT+QICFG="udp/sendmode"` | UDP 送出採 block 或 stream 模式 | TCP-IP | 與 udp/readmode 共用同一組 <mode> 定義。同理，只在做 UDP 時有價值。 |
| `AT+QICFG="viewmode"` | 收到資料的表頭與內容是否同一行 | TCP-IP | 0 = 表頭\r\n資料、1 = 表頭,資料。只影響輸出排版與解析。工具若要自動解析 QIRD 輸出，應該在程式內固定成一種而不是開按鈕給使用者亂按 —— 讓使用者改格式反而會打壞… |
| `AT+QICFG="wakeup/data"` | 設定喚醒封包內容（低功耗用） | TCP-IP | v1.4 才新增的功能，配合低功耗（休眠喚醒）情境，觸發時報 +QIURC: "wakeup/data",<connectID>。手冊 §2.3.1 NOTE 2 白紙黑字寫會丟棄… |
| `AT+QICSGP=?` | 查 context 參數的支援範圍 | TCP-IP | 回傳 contextID、context_type、authentication 等的支援範圍。手冊已把值域寫死（cid 1–15、type 1–3、auth 0–3），實測價值不… |
| `AT+QIOPEN=?` | 查 socket 型別與各參數的支援範圍 | TCP-IP | 回應會列出 "TCP/UDP/TCP LISTENER/UDP SERVICE" 四種字串以及各參數範圍 —— 在動手實作伺服器端功能「之前」，這是最便宜的可行性驗證：先確認 EG… |
| `AT+QIOPEN（access_mode=2 透傳）` | 開連線並直接進入透傳資料模式 | TCP-IP | 透傳是模組最像「一條網路線」的模式，示範價值高（貼上文字就直接進網路），但對一個以 AT 指令為核心的網頁工具是雙面刃：使用者一旦誤入就以為程式當掉。要做的前提是先完成 +++ 逃… |
| `AT+QISDE` | 控制 QISEND 是否回顯輸入的資料 | TCP-IP | 只有在實作了 AT+QISEND 資料模式之後才有意義：關閉回顯（0）畫面比較乾淨，開啟（1）則可以確認模組到底收到了什麼位元組 —— 送二進位資料除錯時後者其實有用。有讀取形式 … |
| `AT+QISTATE=0,<contextID>` | 只列出某個 context 底下的 socket | TCP-IP | 工具目前只用 context 1，全列跟按 context 列的結果一樣。要等到支援多 context（手冊允許同時 3 個）才有價值。 |
| `AT+QISWTMD` | 切換 socket 的資料存取模式 | TCP-IP | 切 0（buffer）/1（direct push）是安全且有用的：direct push 讓收到的資料直接吐到終端機上，不用一直按 QIRD，對「看終端機做判斷」的手動測試其實很… |
| `AT+QNTP?` | 查詢對時進行中的伺服器與埠 | TCP-IP | 只在「對時進行中」才回 +QNTP: <server>,<port>。因為 QNTP 本身最長會擋 125 秒，這條實務上得從另一個 AT 口才下得了 —— 對單口 UART 工具… |
| `ATO` | 回到先前的透傳模式 | TCP-IP | 只有做過透傳、用 +++ 退出之後才有意義（等同於 QISWTMD=<cid>,2 的捷徑）。優先度低於 +++，要收也是跟整組透傳功能一起收。 |
| `AT+QISWTMD` | 切換已建立連線的資料存取模式 | TCP/IP（既有頁簽） | 屬 TCP/IP AN。SSL §1.4 說明連線建立後可用它在 buffer/direct push/transparent 三種模式間切換。對這個工具的價值有限且風險偏高——切… |
| `AT+QWIFISCAN=4000,1,4,0,1` | 全參數最小值的極速掃描，用來診斷掃描引擎是否真的會動 | WiFiScan | 不是文件新指令，只是既有自訂形式的一組參數。列為可選而非建議補，是因為工具的「Scan (custom)」已有五個可編輯欄位，使用者自己填就到得了。但它對目前的 URC 不回報異常… |
| `AT&D1` | 設定 DTR 拉高時脫離資料模式 | 固定區（頁簽外） | 三份文件都說「若要用 DTR 脫離資料模式，必須先設 AT&D1」。Web Serial API 確實能用 setSignals({ dataTerminalReady }) 控制… |
| `ATO` | 回到先前的透明傳輸/資料模式 | 固定區（頁簽外） | 三份文件都提到，但適用範圍支離破碎，做成按鈕反而容易誤導：SSL 透明傳輸模式可用 ATO 回去；FTP 的 QFTPGET/QFTPLIST/QFTPNLST 之後可以，QFTP… |
| `AT+QSSLCFG` | 設定 MQTT over TLS 用的憑證、版本、cipher、seclevel | 新頁簽：SSL / File | 本文件只在 §5.2 範例中引用（cacert / clientcert / clientkey / seclevel / sslversion / ciphersuite / i… |
| `AT+QCFG="ims"` | 設定 IMS 功能開關並查詢 VoLTE 支援能力 | 未指定 | 查詢形式回 <IMS_conf>,<VoLTE_cap>，能一眼看出這顆模組是否支援 VoLTE，對確認韌體能力有點價值。<IMS_conf> 0=未配置、1=啟用、2=停用（EG… |
| `AT+QCFG="roamserviceex"` | 設定漫遊狀態下停用撥號上網／語音的位元遮罩 | 未指定 | 範圍 0–3 的位元遮罩：Bit 1=漫遊時停用撥號上網、Bit 2=漫遊時停用語音、3=兩者皆停、0=不限制。只有拿漫遊 SIM 做跨境測試才用得到，實驗室測試幾乎碰不到。手冊另… |
| `AT+QCFG="uart2ipr"` | 設定 UART2 的鮑率 | 未指定 | 只管 UART2（EG800K 上通常是 debug／輔助口），本工具接的是主 UART，改它不影響目前連線。支援值 4800–921600。除非專案另外要用 UART2 接周邊，… |
| `ATH` | 掛斷現有連線（資料或語音） | （僅在補入 ATD/ATA 後才需要） | 唯一值得考慮的理由是當作「誤入資料模式後的救援鍵」——先 +++ 回命令模式、再 ATH 掛掉連線。但本工具不提供 ATD / ATA / AT+CGDATA，正常操作不會產生要掛… |
| `AT+CMGF` | 設定簡訊 PDU 模式或文字模式 | （若新增 SMS 頁簽） | 純前置設定：所有可讀的 SMS 指令都要先 AT+CMGF=1 才會輸出人看得懂的文字。本身無驗證價值，只有在真的做 SMS 頁簽時才需要。手冊 Characteristics 欄… |
| `AT+CMGL` | 依狀態列出儲存區內的簡訊 | （若新增 SMS 頁簽） | AT+CMGL="ALL" 是驗證「簡訊收得到嗎」最直接的一條。但有兩個坑要在 tip 標明：一是不帶參數的 AT+CMGL 只列未讀、二是列出後未讀會被標記為已讀，對正在除錯的人… |
| `AT+CMGR` | 依索引讀取單一封簡訊內容 | （若新增 SMS 頁簽） | 需要一個 <index> 參數欄（工具已有 params 機制可支援）。搭配 AT+CSDH=1 可看到完整表頭（SMSC、時間戳、DCS），對除錯有用。但實務上先 AT+CMGL… |
| `AT+CNMI` | 設定新簡訊如何通知到 TE | （若新增 SMS 頁簽） | AT+CNMI=2,1,0,0,0 會讓每封新進簡訊在終端機吐出 +CMTI: "SM",<index>，是「證明這張卡收得到簡訊」最直觀的示範，而且不需要 Ctrl+Z。若改用 … |
| `AT+CPMS` | 查詢/選擇簡訊儲存區與使用量 | （若新增 SMS 頁簽） | AT+CPMS? 一次回三組 <mem>,<used>,<total>（讀取區/寫入區/接收區），可直接看出「SIM 的 50 格簡訊是不是滿了」——儲存滿是收不到新簡訊的典型原因… |
| `AT+CSCA` | 查詢/設定簡訊中心 SMSC 位址 | （若新增 SMS 頁簽） | Read form（AT+CSCA?）有真實診斷價值：SMSC 為空或號碼錯誤是簡訊送不出去最常見的原因之一，唯讀無副作用。寫入形式不建議做成按鈕。與 CSMS? 一樣，只有在打算… |
| `AT+CSDH` | 控制文字模式簡訊是否顯示完整表頭 | （若新增 SMS 頁簽） | 純顯示開關：AT+CSDH=1 之後 AT+CMGR / AT+CMGL 會多吐出 SMSC 位址、<fo>、<dcs>、<vp> 等欄位，對除錯簡訊編碼問題有幫助。無副作用、設定… |
| `AT+CSMS` | 查詢/選擇簡訊服務類型與支援能力 | （若新增 SMS 頁簽） | AT+CSMS? 回 <service>,<mt>,<mo>,<bm>，是判斷「這顆韌體 / 這張卡到底支不支援收發簡訊」最便宜的一條指令，唯讀、300 ms、無副作用。第 9 章… |
| `AT+QCEERCATCFG` | 切換 AT+CEER 的回應格式 | （需與 §4.2 AT+CEER 一起補） | 設 <mode>=1 之後 AT+CEER 會從一句字串變成 +CEER: <category>,<cause>,<description> 的結構化輸出（例："EMM attac… |

## §5 不建議收錄（97 條）

**逐條都有判定理由**，不是略過不看。以下依原因歸類，完整清單見 §8 附錄。

- **會讓 AT 口失效／自傷**（18 條）：`AT+QWIFISCAN=255000,6,30,255,1`、`AT+QINDCFG="datastatus"/"mode"/"sm`、`AT+QMTCFG="willex"`、`AT+QFUPL`、`ATA`、`ATD`、`ATO`、`ATS0`、`AT+CGDATA`、`AT+QNETDEVCTL`、`ATQ`、`ATS3`…
- **實際射頻發射／法規風險**（2 條）：`AT+QRFTEST=<band>,<TX_channel>,"on`、`AT+CLCC`
- **與現有指令完全重疊**（5 條）：`AT+QGPS=0`、`AT+CGMI`、`AT+CGMM`、`AT+CGMR`、`AT+CGSN`
- **語音／簡訊／電話簿（本工具無此功能）**（17 條）：`AT+COLP`、`AT+CHUP`、`AT^DSCI`、`AT+CPBF`、`AT+CPBW`、`AT+CMGD`、`AT+CMGS`、`AT+CMMS`、`AT+CMGW`、`AT+CMSS`、`AT+CNMA`、`AT+QCMGS`…
- **legacy／2G3G 遺產**（8 條）：`AT+CSMP`、`AT+CGQREQ`、`AT+CGQMIN`、`AT+CGEQMIN`、`AT+CGCLASS`、`AT+QPPPDROP`、`AT+CSIM`、`AT+CGACT`
- **其他（本工具情境用不到）**（41 條）：`AT+QGPSCFG="ntp",<server>`、`AT+QGPSEND=?`、`AT+QGPSEND?`、`AT+QGPSLOC=?`、`AT+QAGPSCFG=<profile>[,<URL>[,<ven`、`AT+QGPSVBCKP=1`、`AT+QRFTESTMODE=1`、`AT+QRFTESTMODE=0`、`AT+QRXFTM=?`、`AT+QRXFTM=<band>,<RX_channel>,"on"`、`AT+QRXFTM=<band>,<RX_channel>,"off`、`AT+QRFTEST=?`、`AT+QRFTEST=<band>,<TX_channel>,"of`、`AT+QMTCFG="aliauth"`…


---

## §6 重大發現

以下 11 項是本次盤點中**比「補幾顆按鈕」更重要**的發現。

### 6.1 URC 預設不走 UART —— 可能讓三個頁簽整組失效 🔴

低功耗應用筆記 §5.4.2 原文：「The host can configure the URC-reporting port by AT+QURCCFG …
**The default port is USB AT port**」。AT 手冊 §2.24 的查詢範例也顯示 `+QURCCFG: "urcport","usbat"`。

**這代表若模組維持出廠預設，走 UART 的本工具一條 URC 都收不到。**
GNSS 頁的定位 URC、TCP/IP 頁的 `+QIURC`／`+QIOPEN` 非同步結果、MQTT 頁的 `+QMTRECV`／`+QMTSTAT`
全部會靜默，而使用者看到的症狀是「指令都回 OK，就是永遠等不到訊息」——
用現有 66 條指令**完全查不出原因**。

同理還有 `AT+QCFG="urc/cache"`：若被設成 1，URC 會被壓住不即時輸出。

> **建議**：連線成功後自動跑一次 `AT+QURCCFG="urcport"`，不是 `uart1` 就跳提示。
> 這是本次盤點中最該優先處理的一條。

### 6.2 MQTT 發布指令的懸案結案：現行實作是錯的，但修得好 🔴

我們一直存疑的 `AT+QMTPUBEX` 末參數，答案明確：**是「長度」不是「訊息內容」**。四個獨立證據：

1. §3.3.8 標題句「This command publishes **fixed-length** messages…」
2. 寫入式語法 `AT+QMTPUBEX=<client_idx>,<msgid>,<qos>,<retain>,<topic>,<length>`，
   Response 欄第一行就是 `>`，接著「After > is reported, input the data to be sent.」
3. 參數表「`<length>` **Integer type**. Length of message to be published.」
4. 測試式回應 `+QMTPUBEX: (0-5),<msgid>,(0-2),(0,1),"topic","length"`

**所以現行的 `AT+QMTPUBEX=0,0,0,0,"{topic}","{message}"` 送出去只會得到 ERROR。**

但好消息是：**QMTPUBEX 不需要 Ctrl+Z**（與 `AT+QISEND` 不同）。它是固定長度協定，
模組數滿 `<length>` 位元組就自動送出。所以本工具「送不出 0x1A」不構成障礙，只要做成兩段式：

```
送 AT+QMTPUBEX=0,0,0,0,"topic",30   →  等模組吐 '>'  →  送剛好 30 bytes（行尾必須切成 None）
```

⚠️ 實作陷阱：`sendData()` 目前一律把行尾字元接在送出內容後面，
payload 階段必須繞過這段邏輯，否則多出來的 CR 會被算進長度而錯位。

另外兩點：`<msgid>` 在 SUB/UNS 是 1–65535（不含 0），在 PUBEX 是 0–65535 且「只有 qos=0 時才可為 0」；
最壞阻塞時間不是 15 秒而是 **600 秒**（`<pkt_timeout>` 最大 60 × `<retry_times>` 最大 10）。

> **📌 2026-08-02 追記：本項已於實機確認並修復（V26.0.22）。**
> `AT+QURCCFG="urcport"` 實測回 `"usbat"` —— 模組確實把 URC 全部送到 USB 埠。
> 切成 `uart1` 後，困擾兩天的 Wi-Fi Scan「韌體 bug」當場消失（見 §6.3 追記）。
> 設定寫 NVRAM，重開機後仍為 uart1。工具已新增 URC 診斷組並在註解直接示警。

### 6.3 Wi-Fi Scan 掃不到的原因分析

硬體設計手冊 §5.1 與規格書註 2：**Wi-Fi Scan 與主天線共用 `ANT_MAIN`（pin 35），時分複用，
兩種功能不可同時使用**。若控制板的 ANT_MAIN 未接天線、或匹配網路只針對目前掛的
LTE Band 8（900 MHz）調諧，2.4 GHz 靈敏度會極差。

**但這只能解釋「掃不到熱點」，解釋不了「連 TIMEOUT 都沒有」** ——
文件明說掃不到就該回 `+QWIFISCAN:TIMEOUT`。所以天線頂多是次要因素。

> **📌 2026-08-02 追記：真正原因是 §6.1 的 URC 埠，不是天線也不是韌體。**
> 上述排查順序**一步都不必跑**。`AT+QURCCFG="urcport","uart1"` 之後立刻掃到 5 個熱點：
> ```
> +QWIFISCAN: (-,-,-35,"C2:28:35:00:00:01",1)
> +QWIFISCAN: (-,-,-50,"62:62:DE:00:00:05",1)
> +QWIFISCAN: (-,-,-67,"98:25:4A:00:00:06",8)   …共 5 筆
> ```
> 天線共用 ANT_MAIN 的事實仍然成立（會影響靈敏度），但它從來不是「連 TIMEOUT 都沒有」的原因 ——
> **TIMEOUT 本身也是 URC，一樣被送到 USB 埠了**。這是當初分析時沒想到的一層。
>
> 原本的排查順序保留在下方供參考，但已證實不適用於本案：

1. 最小掃描 `AT+QWIFISCAN=4000,1,4,0,1`（4 秒一輪，可快速反覆試）
2. `AT+CFUN=4` 關掉蜂巢 RF 放開天線後再掃 → 測完 `AT+CFUN=1` 復原
3. 檢查控制板 ANT_MAIN 是否真的接了天線
4. 以上都仍只回 OK → 高度確定是韌體 build 缺功能，走 Quectel FAE 換韌體

附帶：現有參數 tip 寫的範圍（round 1–3、maxbssid 4–10）是舊版 v1.1 的值，
**v1.2 已改為 round 1–6、maxbssid 4–30**。但真正該信的是本機 `AT+QWIFISCAN=?` 的實際回應。

### 6.4 解析器陷阱（Wi-Fi Scan）

- **括號不一致**：語法定義寫 `+QWIFISCAN: <ecn>,<ssid>,…`（無括號），
  但兩份文件的範例輸出都帶括號 `+QWIFISCAN: (-,-,-30,"1C:20:…",1)`。解析器兩種都要吃。
- **冒號後空白不一致**：結果行是 `+QWIFISCAN: `（有空白），逾時行是 `+QWIFISCAN:TIMEOUT`（**沒有空白**）。
  用統一前綴比對會漏掉 TIMEOUT。

### 6.5 逾時：至少 14 條指令遠超一般值，需要 per-command timeout

工具目前對所有指令沒有個別逾時設定。手冊標示的最大回應時間差距極大：

| 逾時 | 指令 |
|---|---|
| 600 s | `AT+QMTSUB` / `AT+QMTUNS` / `AT+QMTPUBEX`（最壞情況） |
| 300 s | `AT+COPS=?`（掃全網）、`AT+CGEQREQ` |
| 150 s | `AT+CGACT`、`AT+QIACT`、六條 `AT+QCFG` 子項 |
| 140 s | `AT+CGATT` |
| 120 s | `AT+QMTOPEN`、`AT+CMGS` 系列 |
| 50 s | `AT+QDSIM` |
| 15 s | `AT+CFUN` |
| 5 s | `AT+CPIN`、`AT+CLCK`、`AT+CPWD` |

> **建議**：在指令定義加 `timeout` 欄位。否則使用者會看到「指令沒反應」，但模組其實還在跑。

### 6.6 會讓 AT 口失效的指令（絕對不要做成按鈕）

| 指令 | 後果 | 能否救回 |
|---|---|---|
| `ATQ1` | 模組完全不回結果碼，工具每條指令都判逾時 | 盲打 `ATQ0`，且無任何回饋 |
| `ATV0` | `OK` 變成 `0`、拿掉前導 CR LF，回應解析全爛 | 盲打 `ATV1` |
| `ATS3=<n>` | 改掉命令列結束字元，工具送的 CR 不再被辨識 | **幾乎只能斷電重開** |
| `ATS4=<n>` | 改掉回應格式字元，分行解析全爛 | 同上 |
| `ATA` / `ATD` / `ATO` / `AT+CGDATA` | AT 口變資料通道 | 需 `+++`（見下） |
| `AT+QSCLK=1` | 模組可能立刻睡著不回應 | 拉低 DTR 喚醒 |
| `AT+QRFTEST=…,"on",…` | **實際射頻發射**，法規與干擾風險、可能燒 PA | 先 `"off"` 再退 FTM |

⚠️ **本工具目前連 `+++` 逃生都做不到** —— `+++` 要求前後各 1 秒靜默且**不可帶 CR/LF**，
而現行 `sendData()` 一律加行尾字元。若日後要收錄任何進資料模式的指令，
**必須先實作裸位元組送出與 guard time**。

### 6.7 訊號品質有真空：完全沒有 RSRP / RSRQ / SINR

現有 66 條裡取得訊號的手段只有 `AT+CSQ`（RSSI + BER，且 BER 在 LTE 恆為 99）
與 `AT+QNWINFO`（制式／頻段／頻點，無品質指標）。

`AT+QINDCFG="sqi",1` 開啟後模組主動推 `+QIND: "SQI",<RSRP>,<RSRQ>,<SINR>`，
做天線比較、擺位測試、弱訊號驗證時，這三個值比 CSQ 有用一個量級。
同理 `AT+QINDCFG="csq",1` 可把訊號量測從「狂按 AT+CSQ」改成推播。

### 6.8 `AT&V` 是唯一能讀出單字母參數的指令

`ATE`／`ATQ`／`ATV`／`ATX`／`AT&C`／`AT&D` 這些都**沒有各自的讀取形式**（沒有 `ATE?` 這種東西）。
只有 `AT&V` 能一次 dump 出全部目前值。接手一顆被前人亂設過的模組時，這是第一條該下的指令。

### 6.9 3GPP PDP 層 vs Quectel 堆疊層，兩者可能不一致

`AT+CGACT?` / `AT+CGPADDR` / `AT+CGDCONT?`（3GPP PDP 層）與現有的
`AT+QIACT?` / `AT+QICSGP`（Quectel 內建 TCP/IP 堆疊層）是**不同層次**：
模組可能已在 3GPP 層拿到 IP 但 Quectel 堆疊尚未啟動，反之亦然。

兩組並排呈現，能讓工程師一眼分辨故障在**網路側**還是**模組協定堆疊側**。
這是補入第 10 章那幾條唯讀指令最大的價值。

### 6.10 SMS 頁簽的架構前提

第 9 章 SMS 共 18 條。`AT+CMGS` / `AT+CMGW` / `AT+QCMGS` 全是「先回 `>`、再送內文、最後送 Ctrl+Z」
的兩階段指令，而 SMS **沒有**像 `AT+QISENDEX` 那樣的單行替代形式。

> 結論：在終端機取得裸位元組送出能力之前，SMS「發送」在架構上不可能實作；
> 只有讀取類（`CMGL`／`CMGR`／`CPMS?`）與 URC 類（`CNMI`）可行。
> 要做 SMS 頁，**第一步是改終端機，不是加指令陣列**。

### 6.11 RF FTM 其實支援 EG800K —— 但仍然不收

檔名 `quectel_ec200xeg912yeg915n_series_rf_ftm…` 讓人以為不適用 EG800K，
但 PDF 封面實為 v1.3，§1.1 Table 1 **明列 EG800K Series**（v1.3 修訂記錄寫「Added … EG800K series」）。

**不收錄的理由是用途錯位與安全，不是機型不支援** —— 這個區別要寫對，別在文件裡誤導。
FTM 是產線 RF 校準模式（需綜測儀與屏蔽箱），且 `AT+QRFTEST=…"on"` 會**實際輻射射頻功率**。

附帶：手冊全文搜尋 `CPSMS` / `CEDRX` / `PSM` / `eDRX` **零命中** ——
這個系列的官方文件根本沒有 3GPP PSM 與 eDRX 指令，本系列的「低功耗」是 DRX + DTR 閘控的模組睡眠。
別憑既有 Quectel 知識腦補這兩個功能。

---

## §7 建議執行順序

分四批，每批都是可獨立驗收的完整單位。

> **執行結果（2026-08-02 補記）：四批全部完成。** 指令數 61 → **189**、頁簽 6 → **9**。
> 對應版本：第 1 批 V26.0.22、第 2 批 V26.0.23、第 3 批 V26.0.24、第 4 批 V26.0.25~26。
> 唯一未結案的是**真實數據連線實測**（漫遊費待 user 裁決），已移入 `TODO.md`。
>
> 執行過程中推翻了報告的兩個判斷：
> - §6.3 原判「Wi-Fi Scan 結果 URC 不回報」疑似韌體缺陷 —— **實際是 `urcport` 出廠值為
>   `usbat`**，結果 URC 全被送到 USB 埠。切 `uart1` 後立刻正常。§6.1 的預測是對的，
>   但沒料到它同時解釋了 §6.3
> - 第 4 批預估「73 條」，實際做出 **98 條**（三份文件的指令數比初次掃描多）

> **數據連線實測結案補記（2026-08-08）：本報告唯一未結案的項目已完成大半。**
> 2026-08-05 user 裁決同意產生漫遊流量，隨即依 `reports/data-connection-test-plan.md`
> 分 P1–P8 開跑。到 2026-08-08 為止：
>
> | 階段 | 結果 |
> |---|---|
> | P1 診斷三件套 | ✅ 全通過（`reports/data-connection-test-plan.md` §3） |
> | P2 TCP socket | ✅ 收發主路徑通過；2-5～2-9 未做 |
> | P3 HTTP / HTTPS | ✅ **10 項全數通過**（`reports/p3-http-test-procedure.md`）|
> | P4 MQTT | ⏳ 註解已補齊，連線實測未跑完 |
> | P5 SSL raw socket | ✅ **10/10**（`reports/p5-ssl-test-results.md`）|
> | P6 FTP | ✅ 8 通過 / 1 部分（`reports/p6-ftp-test-results.md`）|
> | P7 定位 | ⏳ 3 完成 / 2 待天空視野 / 4 待 QuecLocator token（`reports/p7-location-test-results.md`）|
> | P8 收尾 | ✅ 2026-08-08 |
>
> **實測推翻了本報告與手冊的若干判斷**，重點三條（完整清單見
> `.claude/skills/EG800K_Modem_SKILL.md` §4 與 §5.1–5.4）：
>
> - **「本工具送不出憑證，所以 `seclevel` 1/2 必定失敗」是錯的** —— PEM 是純 ASCII，
>   `AT+QFUPL` 可以直接從 AT 埠把憑證寫進 UFS，2026-08-07 已上傳 1,939 bytes 的 ISRG Root X1
>   並以 2×5 對照證明憑證驗證確實在動
> - **`AT+QFTPCFG="account"` 查詢時密碼被模組遮成 `*`**，與手冊「回應會把密碼原樣印出」相反。
>   主程式四處沿用手冊說法的文字已於 V26.0.77 全部改成實測說法
> - **`+++` 對 FTP 資料模式是「中止」不是「暫停」**，`ATO` 續不回來（`NO CARRIER`），
>   與 FTPS 應用筆記 v1.5 p13 明文不符
>
> 另外實測出一個本報告完全沒有預料到的類別：**資料堆疊退化**（連續操作後
> 所有連線一律失敗，但每項自我檢查都說正常，只有完整開機儀式能復原）。
> 鑑別方法與因應寫在技能檔 §5.1。

### 第 1 批：修正既有錯誤（最優先，因為是「現在就是錯的」）

1. **修 `AT+QMTPUBEX`** —— 改成兩段式（送指令 → 等 `>` → 送 N bytes、行尾 None）。
   現行單行版必定失敗，屬於已知 bug（§6.2）
2. **加 `AT+QURCCFG="urcport"` 查詢**並納入連線後自動健檢（§6.1）
3. **修 Wi-Fi Scan 的參數範圍與解析器**（v1.2 新範圍、括號與空白兩個陷阱，§6.3／6.4）
4. **加 per-command timeout 欄位**（§6.5）

### 第 2 批：零風險唯讀診斷（投報率最高，全部 300 ms 以內）

`AT&V`、`AT+CEER`、`AT+QINISTAT`、`AT+QSIMSTAT?`、`AT+CGATT?`、`AT+CGPADDR`、
`AT+CGACT?`、`AT+CGDCONT?`、`AT+QGDCNT?`、`AT+QLTS=2`、`AT+QSCLK?`、`AT+QURCCFG=?`

建議新增分組：Hardware 頁「Serial」與「URC」、Basic 頁「Diagnostics」與「PDP」。

### 第 3 批：功能性補充（有副作用，要警告文字）

`AT+CFUN=` 寫入形式（0/1/3/4/5 + `1,1` 需二次確認）、`AT+CMEE` 切換、`AT&F`、
`AT+QINDCFG="sqi"/"csq"`、`AT+CGATT=` 寫入形式、`AT+COPS=?`（300 秒 + 中斷業務警告）

### 第 4 批：新功能領域（要新頁簽，工程量大）

SSL / HTTPS / FTPS 三份文件共 73 條，且三者有依賴關係（HTTPS/FTPS 都要先用 `AT+QSSLCFG` 設好憑證）。
建議先做 **SSL 獨立頁簽**（它是被另兩者引用的共用層），HTTP 與 FTP 可合併為一頁。
⚠️ 這批全部需要真實數據連線，本機 SIM 是國際漫遊卡，**開跑前請先確認漫遊費用**。

> **實作結果**：做成 **SSL 22 / HTTP 36 / FTP 36 三個獨立頁簽**（沒有合併 HTTP 與 FTP ——
> 兩者各 36 條，塞同一頁會需要大量捲動）。
>
> **漫遊費問題用「零流量驗證」繞過**：`AT+Qxxx=?` 測試形式不觸網，34 條指令逐一探測全部存在，
> 三個 CFG 指令的參數 key 也逐一比對韌體回報清單 —— 沒有一條是別顆模組才有的。
> 這招抓到一個真錯誤：**`AT+QHTTPREAD` 本機韌體只吃一個參數**，應用文件的
> `<wait>,<read_len>` 分段讀法實測回裸 `ERROR`，那兩顆按鈕已移除（V26.0.26）。
> 手法與陷阱記在技能檔 §4.6。真實連線實測仍待 user 裁決漫遊費。

---

## §8 附錄：完整判定清單

413 條的逐條原始資料（含每條的判定理由、風險、章節、逾時）保存於盤點工作區的
`audit.json`，本報告的 §3–§5 表格即由該檔產生。若需要查某條指令為何被判「不建議」，
以指令名搜尋該檔的 `reason` 欄位即可。

### 與本報告相關的專案文件

- `.claude/skills/EG800K_Modem_SKILL.md` —— 硬體開機程序、AT 指令實測記錄、註解表擴充指南
- `changelog.md` —— V26.0.7～V26.0.9 記錄了現有 6 頁簽的建立過程
- `CLAUDE.md` §硬體參考資料 —— 已同步更新為 16 份 PDF（原記載 7 份）
