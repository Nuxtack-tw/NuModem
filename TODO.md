# TODO

> 版號制度：`Va.b.c`（a = 西元年後兩碼、b = 版本釋出（user 宣布釋出才 +1）、c = 功能擴充與 bug 修正），唯一來源為主程式 `<title>`。
> 改動前務必先備份：`cp NuModem_EG800.html backup/NuModem_EG800_V<目前版號>.html`

## 進行中

### user 人工驗收非連線功能（2026-08-05 起，**優先於連線測試**）

清單：**`reports/offline-acceptance-checklist.md`**（A-G 七區 35 項＋8 個測試陷阱）。
發現的問題隨到隨修；驗收完才開跑下面的連線測試。

### 數據連線實測（2026-08-05 user 同意產生漫遊流量；**暫停，等上面驗收完**）

計劃全文與逐項狀態：**`reports/data-connection-test-plan.md`**（此處只掛階段，細項勾稽在計劃內）

- [x] ~~P1 TCP/IP 診斷三件套~~ **2026-08-06 完成**（QPING/QIDNSGIP/QNTP 全通、註解已補 V26.0.52）
      —— 排障發現：本卡單一 PDP 且自動 context 編號浮動，需先 CGACT=0 讓位再 QIACT=1
- [x] ~~P2 前置：測試對端怎麼來~~ **2026-08-06 定案** —— user 提出消費者不能改 router 的產品約束，
      結論是**不開埠、走免費公開服務**（模組是 TCP client，只需要一台從外網連得到的伺服器）。
      **V26.0.58 只套用到 TCP/IP 頁**（`AT+QIOPEN` → `tcpbin.com:4242`）；
      路由器自動開埠三協定（UPnP／NAT-PMP／PCP）本機實測全滅，工具 `tools/nat_probe.py` 保留備用
- [ ] P2 TCP socket 收發（**tcpbin.com:4242**，已是內建預設）
  - [x] ~~2-1～2-4 收發主路徑~~ **2026-08-07 實機驗證通過**（Send Text 與 Send Var 連續送出兩路都收到 echo）
  - [x] ~~`+QIOPEN` 結果 URC 註解~~ **V26.0.59**（含 `TCPIP_ERRORS` 表）
  - [x] ~~P2 回應行註解~~ **V26.0.60**：`+QIRD:`（兩形）、`+QISEND:`、`+QIGETERROR:`、`+QISTATE:`
  - [ ] **剩餘測項**：2-5 查緩衝、2-6 關閉、2-7 異常路徑、2-8 對端斷線（tcpbin 15 秒逾時即可，不必自架）、
        2-8b 收到 closed 後直接 QIOPEN 應回 563、2-9 被動接收（需自架 `tools/tcp_test_server.py` ＋ bore 通道）
- [x] ~~P3 HTTP / HTTPS~~ **2026-08-07 實機全數通過（10 項）**；
      **可自行照做的完整流程：`reports/p3-http-test-procedure.md`**：GET／READ／GETEX 逐 byte／POST 回吐／
      HTTPS／DNS 異常／404／回應標頭／轉址。查出 3 個 bug（V26.0.68 修）與 3 個手冊未寫的行為
- [ ] P4 MQTT（**QMTPUBEX 兩段式自迴路 = 核心驗收**）
  - [x] ~~補 `+QMT*` 註解~~ **V26.0.71**：7 張對照表 + 11 條 URC 規則。
        `+QMTCONN` 第二欄在查詢式是 `<state>`、寫入式是 `<result>`，同一數字兩種讀法 —— 並陳不硬猜
  - [x] ~~**clientid／topic 加隨機尾碼**~~ **V26.0.72**（user 選 A：頁面載入時產生）：
        `numodem-<6 位 hex>` / `test/numodem-<同一組>`，Subscribe／Publish／Unsub 三顆共用。
        ⚠ **每次重新整理換一組** —— 訂閱與發布要在同一次頁面生命週期內完成；
        跨重新整理（例如中途跑開機儀式）就對不起來
- [x] ~~P5 SSL raw socket~~ **2026-08-07 完成，10/10 通過**（`reports/p5-ssl-test-results.md`）
      - 5-9／5-10 做成 2×5 對照：關驗證時五台全連得上、開驗證時只有好憑證過 —— 兩個方向都成立才算數
      - **憑證送得進去**：PEM 是純 ASCII，`AT+QFUPL` 已上傳 1939 bytes 的 ISRG Root X1
      - ⚠ `sni` 出廠預設 0，不開就驗不過；`ignorelocaltime` 出廠預設 1（不檢查有效期）
- [ ] **SSL 連線連續開關約 20 次後資料堆疊會整個退化**（2026-08-07 P5 發現，累計第 4 次遇到模組異常）
      症狀：所有 `QSSLOPEN` 回 552，且**連純 `AT+QIOPEN` 到同一台也回 552**（這是關鍵鑑別方法）。
      此時 `QSSLSTATE` 空、`QIACT?` 有 IP、`QIGETERROR` 回 0，看起來完全正常。
      `QIDEACT`+`QIACT` **救不回來**（QIACT 直接回 ERROR），只有開機儀式能復原。
      待辦：確認觸發門檻是次數還是失敗次數，並考慮在 UI 上做「連線失敗連續 N 次就提示重開機」
- [ ] 考慮在 SSL 頁加「上傳憑證」按鈕（`AT+QFUPL` 兩段式，PEM 純文字可貼）——
      目前 seclevel 1/2 走得完，但要手打指令
- [x] ~~P6 FTP~~ **2026-08-07：8 通過 / 1 部分**（`reports/p6-ftp-test-results.md`）
      - 6-7 改名＋刪除**已於同日補做完成**：`+QFTPRENAME: 0,0`、`+QFTPDEL: 0,0`，前後 SIZE 各自符合預期
      - 6-9 部分：`+++` 逃逸成功，但 **`ATO` 無法續傳（NO CARRIER）**，與手冊不符
      - 6-10 FTPS explicit 為選測，未做
- [~] P7 定位加速與網路定位 **2026-08-07：3 完成 / 2 無法測 / 4 卡 token**
      （`reports/p7-location-test-results.md`）
      - ✅ 7-1 AGNSS 現況、7-6 QLBS 組態、**7-11 QLBS 按鈕群與註解（已備妥）**
      - ✅ ~~7-2～7-4~~ **2026-08-29 完成**（user 換主動式天線後由 Claude 全程自動執行）：冷啟動 95.0 秒 → ＋AGNSS 51.5 秒（−46%）
      - ⛔ 7-7～7-10：**要先向 Quectel 申請 QuecLocator token** —— 這件事只有 user 能辦
- [x] ~~定位這條線~~ **2026-08-29 收尾（user 裁示）：基地台定位 71 m 為結論**。
      完整結論見 `reports/cell-wifi-positioning-options.md` **§8**。
      指令：`python tools/wifi_geolocate.py <掃描檔> --provider unwiredlabs --key <金鑰> --mode cell`
      ⚠ **71 m 是「查表命中」不是量測精度** —— 連續三次回完全相同座標；
      同一 cell 永遠回同一點，換基地台／換地點誤差會重骰（服務自報 ±1051 m 才是它的不確定性估計）。
      **要當產品指標必須多地點重測取分布，不可外推**
- [ ] **Wi-Fi 網路定位：擱置（卡供應商，非技術問題）**。方法與工具都就緒，隨時可恢復：
      - 願意綁卡（額度內免費、不會扣款）→ `--provider google`，工具直接可用
      - WiGLE 若恢復註冊 → 要補 `--provider wigle`（單顆 BSSID 查已知位置，模式不同）
      - 願意公開自家 AP＋座標 → geosubmit 回報 beaconDB（**隱私代價，需 user 明確裁示**）
      2026-08-29 查證：MLS 已停服、beaconDB 本區無涵蓋、Unwired 免費方案不含 WiFi、
      HERE 2025-08-31 起取消免卡方案 —— **「免費＋免綁卡＋有臺灣涵蓋」的服務已不存在**
- [~] **QuecLocator：不採用**（2026-08-29 user 裁定，理由見
      `reports/cell-wifi-positioning-options.md` **§9**）。
      **不是因為它比較可能倒，是因為它把供應商鎖在韌體層** —— 服務一停，
      `AT+QLBS` 直接失效、整個定位流程要重新設計；主機端查表只要換 `--provider`。
      旁證：Quectel 員工論壇明講 BG95 已不再支援；EG800K 官方 16 份文件無一份 QuecLocator。
      → 7-7～7-10 **僅在拿得到免費試用 token 時順手驗證**，不主動投入。
      → 若真需要「裝置自己定位」，走方案 D（模組 `AT+QHTTPPOST` 打自選 API），供應商可換
- [x] ~~把模組帶到窗邊／戶外補測 7-2～7-4~~ **2026-08-29 完成**（`reports/p7-location-test-results.md` 2026-08-29 節）：
      冷啟動 95.0 秒 vs 冷啟動＋AGNSS 51.5 秒（−46%），AGNSS 每次下載 32-34 KB。
      兩個新陷阱：QGPSDEL 是半實作殘根（=? 回 (0-2) 但參數全拒收）；
      AGNSS 約 20 秒會回 nsat=00 的**偽定位**（參考位置注入），真定位判準 nsat>0 且 fix≥2
- [ ] 註解引擎建議：+QGPSLOC 的 nsat=00 偽定位應加警告註解（「這不是真定位」），
      使用者按 Loc 鈕看到座標很容易誤信 —— 順帶 UI 的地圖頁也吃了這筆偽座標
- [ ] `+CME ERROR: DSAT_CME_GNSS_SE_NOT_ACT` 的註解只是照唸代號 ——
      應改成「GNSS 工作階段未啟用，要先下 AT+QGPS=1」
- [x] ~~取得 QuecLocator 官方應用文件~~ **2026-08-29 完成**：已收進
      `../_ref/EG800K/Application Note/quectel_ec200u_eg915u_series_queclocator_application_note_v1-0__NOT-EG800K.pdf`
      （⚠ 適用機型是 EC200U／EG915U **不含 EG800K**，檔名已標註；
      但指令語法與錯誤碼與本機實測相符，可用）
- [ ] **把 QLBS 錯誤碼表 10000–10008 加進註解引擎**（官方文件已取得；
      即使不採用 QuecLocator，**702 的錯誤註解仍必須修** —— 現行說法是錯的）：
      10002 token 不存在／10006 已過期／10003・10004・10005・10008 各種次數上限／
      10001・10007 IMEI 問題。
      ⚠ **順便修正現有的 702 註解** —— 它是「伺服器逾時未回應」不是 token 問題
- [x] ~~P8 收尾~~ **2026-08-08 完成**：
      - 流量總帳 → `reports/data-connection-test-plan.md` §8。
        **結論是「拿不到總帳」** —— `QGDCNT` 重開機歸零，而 `QAUGDCNT` 名字像累計、
        實際是「每幾秒存進 NV」的間隔（範圍 `(0,30-65535)`、本機出廠 0＝關閉）。
        本專案開機儀式每次重整頁面都要跑，等於斷電幾十次。
        **P2/P3/P4/P6 沒當場記 QGDCNT，那部分永久遺失**；
        後續要拿真總帳只能在測試前先 `AT+QAUGDCNT=30`
      - 技能檔 §4 補 28 條資料連線實測記錄，§5 新增 §5.1 資料堆疊退化／§5.2 `OK` 只代表收下／
        §5.3 對端伺服器慣性／§5.4 錯誤碼 702 命名空間衝突
      - 盤點報告 `reports/at-command-coverage-audit.md` §7 補記結案狀態與三條推翻手冊的發現
      - `MEMORY.md` 更新現況（版本停在 V26.0.61 已過時）、`changelog.md`、本檔

**各協定的預設對端待處理（各自測試階段開跑時才動，不要提前改）**——
候選位址都已實測可連，數據見 `reports/tcp-server-setup.md` §3：

- [ ] P4 開跑時：`AT+QMTOPEN` 主機目前是**空字串**（按下去必然失敗）→ 候選 `broker.emqx.io:1883`
- [ ] P5 開跑時：`AT+QSSLOPEN`×2 目前 `example.com:443`（只驗得到交握）→ 候選 `tcpbin.com:4243` TLS echo
- [ ] P6 開跑時：`AT+QFTPOPEN` 主機是 **`192.0.2.2`**（RFC 5737 文件保留位址，**永遠連不上**，
      從手冊照抄）→ 候選 `test.rebex.net:21`；帳密 `test`/`test` → `demo`/`password`；
      檔名 `test.txt` → `readme.txt`（實測 379 bytes）。上傳要另連 `ftp.dlptest.com`
      （帳號**只能寫 `dlpuser`**，`dlpuser@dlptest.com` 實測回 530）

### P2 期間查出、尚未修的既有缺陷

- [ ] **`writeRaw()` 併發寫入**（2026-08-07 實測撞到，非本次改動造成）：
      每次 `getWriter()`／`releaseLock()` 沒有序列化，兩次寫入重疊會拋
      `Cannot create writer when WritableStream is locked`，而且**靜默失敗**（只在終端機留一行錯誤）。
      人手點按不易觸發，自動化腳本或連點兩顆按鈕就會踩到。修法：加一個寫入佇列（約十行）
- [ ] **模組偶發完全無回應**（2026-08-07 遇到一次）：`AT` 沒有 `OK`、ESC（0x1B）也救不回來，
      發生在一次 `AT+QISEND=0` 回 `ERROR` 之後。重跑開機儀式 7.8 秒後恢復。
      **手冊沒有描述此狀況，原因未明** —— 若再遇到請記錄前後指令序列
- [x] ~~**註解覆蓋率盤點要加掃「回應行」**~~ **V26.0.71 全 10 頁掃完**：102 條回應行樣本、0 條無註解。
      過程留下的教訓：我自己編了四筆假回應格式（`+QSSLSTATE` 的 `"SSL"`、`+QWIFISCAN` 欄位順序、
      根本不存在的 `+QSSLCLOSE: 4,0`、掛錯上下文的 `+QWIFISCAN?`），查手冊才發現現有規則本來就對。
      **驗證樣本要對手冊，不要拿樣本去「修」規則**

### AT 面板多語系（V26.0.60 起）

機制與設計全文：**`reports/i18n-design.md`**

- [x] ~~i18n 基礎設施~~ **V26.0.60**：`L()`／``tt` ` ``／`txt()` 三原語、註解引擎 4 個出口全覆蓋、
      切語言不重建 DOM、翻譯檔按需載入（含降級回繁中）
- [x] ~~主批 1,213 條 × 17 語言~~ **2026-08-07 完成**，17 語言洩漏掃描全部 0 處
- [x] ~~V26.0.62–67 新增的 29 條補譯~~ **2026-08-07 完成**，17 語言洩漏掃描全部 0 處（目錄 1,258 條）
- [ ] 翻譯落地後逐語言**目視**抽查（機器驗過鍵完整性與佔位符，但版面爆行、斷詞、
      專有名詞語感只有人眼看得出來 —— 尤其 de/ru 的長複合詞、th/hi 的斷行）
- [ ] **主程式的 RTL 版面**（ar-SA／he-IL／fa-IR）：文字會翻譯，但整體版面沒有 `dir="rtl"`。
      這是 fork 時就存在的缺陷（`reports/offline-acceptance-checklist.md` §3.5），本次未解。
      ⚠ **說明書已經做了 RTL**（V26.0.77，表格跟著鏡像、`<pre>`／`<code>` 維持左至右），
      要補主程式時可以直接抄 `doc/src/build.py` 的 `EXTRA_CSS` 那幾條
- [x] ~~V26.0.68–77 新增／改寫的 14 條補譯~~ **2026-08-08 完成**（`tr16`），17 語言洩漏掃描全部 0 處。
      **順帶修好一個一直在漏的根因**：`at_i18n_sources.json` 是瀏覽器匯出的快照，
      改了原文卻沒重新匯出，那幾條就永遠不會進翻譯目錄 —— 現在改成**聯集併回**（只加不減），
      併回後才發現 V26.0.71 起新增的 `CFG_VALUES`／`QMT_*` 等對照表共 37 條從來沒被抽過
- [ ] 主 UI 那套 i18n 與本套是**兩套機制**，未來考慮是否統一（優先度低）


## 待辦

### 功能開發

- [x] ~~應用手冊完工盤點~~ **2026-08-31 完成**（user 指定的最終完工確認）：
      15 份手冊、321 條指令逐條判定 —— **95% 今天就能執行**（170 有按鈕＋135 命令列手動）、
      12 條缺兩段式按鈕（機制既有）、真正無法實現的每條都有明確限制與替代路徑。
      報告：`reports/appnote-coverage-final-audit.md`；
      逐指令明細：`reports/artifacts/appnote-audit-2026-08-31.json`
- [x] ~~補 `AT+QFUPL` 檔案上傳鈕~~ **V26.0.83（2026-08-31）完成**：
      SSL 頁「UFS 檔案」群 —— Upload 選檔卡（二進位可、大小/checksum 自動算並比對）＋
      QFLST/QFLDS/QFDEL 管理鈕＋FILE 錯誤碼 400–426 併入註解引擎。
      功能說明與測試步驟：`reports/qfupl-usage-and-test.md`。
      ✅ **實機測試同日完成**（模組接回後）：上傳/驗證/負向/清場全數通過；實測新知（UFS 280 KB、錯誤碼形式不一致、逾時存檔）已記報告 §5 與技能檔 §4
- [ ] 補按鈕候選（次要，依價值排序，見盤點報告 §6）：
      QSSLSEND 變長續寫／QFWRITE／QHTTPGET 自訂 header／QFOTADL=<URL> 參數卡／
      QuecCell 查詢鈕 3-4 顆／QSCLK=1/0＋DTR 睡眠快捷／willex／UDP SERVICE 送資料變體

- [x] ~~`doc/manual.html` 內容~~ **V26.0.77–78（2026-08-08）：18 種語言、19 張截圖、992 KB**
      （V26.0.78 依 user 指定，替〈AT 指令面板的運作方式〉七個小節各補一張）。
      建置系統在 `doc/src/`（`build.py` 組裝、`check.py` 驗結構、`README.md` 說明流程）；
      繁中是原始語言，其餘 17 種由它翻譯而來。**要改內容改 `doc/src/bodies/`，不要動產出檔**
- [x] ~~🔴 **本專案自身還沒有 LICENSE**（2026-09-01 發現）~~ → **同日完成**：
      user 選 **MIT**，已建 `LICENSE`（Copyright (c) 2026 Nuxtack）。
      ⚠ `LICENSE` 內文維持**標準 MIT 原文不加字** —— GitHub 的授權偵測器（licensee）
      靠比對原文判定，加了自訂條款就會顯示成 'Other' 而非 MIT。
      涵蓋範圍的說明寫在 `NOTICE.md` §6 與 README，不寫進 LICENSE 本身
- [x] ~~🔴 **上 GitHub 前處理真實座標的隱私問題**（2026-08-29 起）~~
      → **2026-09-01 完成**（user 裁示：降精度＋遮蔽＋換圖，保留報告的技術結論）。
      ⚠ **實際範圍是原記載的 14 倍**：不只那 3 個檔，而是 **43 個檔** ——
      AP MAC 與基地台 ECI/TAC 早已烤進 **18 種語言的說明書正文**
      （`doc/src/bodies/` + `doc/src/fragments/` + 產出的 `doc/manual.html`）。處理方式：
      - **AP MAC**（11 顆、116 處）：保留 OUI，後三段改 `00:00:NN` 穩定序號 ——
        同一顆 AP 在任何檔案恆等、不同 AP 仍相異，WiGLE 類資料庫查不到
      - **基地台 ECI/TAC**：換成一眼可辨的佔位值 `ABCDE02`／`1234`，且**算術自洽**
        （0xABCDE02=180149762、>>8=703710、&0xFF=2；0x1234=4660）——
        hex→dec 換算的教學點不受影響，也省去在 18 種語言各加一句免責說明。
        ⚠ 不遮這個的話座標遮了也是白遮：ECI 丟進 beaconDB 就直接回原座標
      - **座標**：定位報告改用 **P0/P1/P2** 標記，不是一律遮成 `22.8xx` ——
        報告靠「兩次查詢回**完全相同**座標」證明 71 m 是查表命中，
        全遮成同一字串會同時殺掉「632 m 與 71 m 是兩個不同點」和「同點恆等」兩個結論
      - **`doc/img/21-map-track.png`**：標頭座標改 `22.8xx`／`120.2xx`、
        地圖區高斯模糊（街名門牌不可辨），軌跡/標記/縮放鈕原樣保留；
        **OSM 署名依 ODbL 保持清晰**。原圖存隔離區未刪
      - 另清掉 `.claude/sessions/2026-08-06.md` 裡直接寫出的鄉鎮名
- [ ] 🟡 **地圖截圖的殘留風險**（2026-09-01）：模糊後路網幾何仍可辨，
      理論上能與 `22.8xx/120.2xx` 這個約 11 km 方框內的圖資比對。
      要歸零就得**重拍**：程式沒有軌跡注入鉤子，但 `+QGPSLOC:` 是從終端機文字解析的
      （`NuModem_EG800.html` 約 6024 行 `updateLocData`），
      可餵合成 URC 在任意公開地點畫出軌跡後重新截圖
- [ ] 說明書的 **21 張**截圖都是**繁體中文介面** —— 其餘 17 種語言的正文翻好了，圖裡的介面還是中文。
      要補的話一種語言 21 張、共 357 張，先評估值不值得（原記「12 張」有誤，2026-09-01 清點更正）
- [x] ~~🔴 **說明書翻譯缺口：9 種語言、25 個頁簽段落未譯**（2026-09-01 起）~~
      → **同日補完**。實際只有 16 段需要翻譯 —— 另外 9 段前一輪已譯好 fragment、
      只是 agent 死在拼接前，補拼即可（零翻譯成本）。
      `check.py` **17/17**；獨立抽驗 18 個正文檔，段落長度全部 ≥ 6000 字元。
      教訓：工作流中斷後**先分辨「沒譯」與「譯了沒拼」**，別整批重跑
- [ ] 🔴 **說明書翻譯缺口：9 種語言、25 個頁簽段落未譯**（2026-09-01 起）
      V26.0.84 重寫的 9 個頁簽段落只譯完 8 種語言，翻譯工作流撞到 session limit 中斷。
      現況：`doc/src/check.py` 8/17 通過，失敗的正是這 9 種 ——
      ms-MY 缺 7 段最嚴重，he-IL 缺 6、fa-IR 缺 4、th-TH 缺 3，
      ar-SA／de-DE／hi-IN／ja-JP／vi-VN 各只缺 ftp 一段。
      **這些語言的正文現在是半新半舊的混合狀態**，發佈前必須補完。
      補完後：`python doc/src/check.py`（要 17/17）→ `python doc/src/build.py`
      → 產出檔的 `<title>` 目前還停在 V26.0.83，重建時會一併更新
- [ ] 🟡 **UI 提示字串內容過期**（2026-09-01 發現）：
      `NuModem_EG800.html` 約 9988 行「⚠ QuecLocator 沒有官方文件收錄在本專案 ref/」——
      (a) `ref/` 已移出專案，(b) 2026-08-08 起 `../_ref/` 就有
      `Quectel_QuecLocator_Application_Note_V3.4.pdf`（適用機型待查）。
      ⚠ **這句原文就是 i18n 的 key**，改字會讓 17 份翻譯全部對不上 ——
      要改就得連 17 語一起重譯，建議併進下一次翻譯批次做
- [ ] 說明書逐語言目視抽查（與下方 AT 面板 i18n 的目視抽查同一件事，一起做）
- [ ] 評估：連線後自動初始化序列（建議至少 `ATE1` + `AT+CMEE=2` + 確認 `AT+QURCCFG="urcport"` 是 uart1，
      前兩者 session-only、modem 重開就消失）
- [x] ~~數據功能實測（要 user 先裁決漫遊費）~~ → **2026-08-05 user 同意開測**，
      已升級為「進行中」的完整測試計劃（見上方），細項見 `reports/data-connection-test-plan.md`
- [ ] GNSS 定位成功測試（窗邊/戶外）→ 併入測試計劃 P7
- [ ] 評估：`AT_CMD_TABS` 的 `label` 欄位自 V26.0.13 按鈕改版後已無使用點，資料暫留待 user 決定去留
- [ ] 評估：`AT+QHTTPCFG="rspout/auto",1` 與 READ 類按鈕做成 UI 互鎖
      （手冊明載 auto_outrsp=1 後 QHTTPREAD／QHTTPREADFILE 一律失敗）
- [x] ~~補 SSL/HTTP/FTP 的 config 查詢回應註解~~ **V26.0.71**：`cfgNote()` 逐鍵解碼
      （同一數字在不同鍵意思天差地遠：`seclevel` 1＝驗證伺服器、`filetype` 1＝ASCII、`transmode` 1＝被動）；
      另加 `rangeNote()` 專門處理 `AT+XXX=?` 的參數範圍列表 —— 那類回應和「目前設定值」長得幾乎一樣，
      最容易被誤讀成「現在設定是 0 到 2」

### 清理（承母專案）

- [ ] 清掉死屬性 `SerialMonitor.maxReconnectAttempts`
- [ ] i18n 重複定義鍵（zh-TW/en-US/ja-JP 各 5 個 terminal.*.tip）
- [ ] 母專案遺留死代碼（稽核清單見 MEMORY）：port-select 家族 CSS、.btn-disconnect、.modal-overlay 家族、12 個零引用 i18n 鍵

### 待決策

- [ ] CDN 白名單：fonts.googleapis.com / flagcdn.com（母專案暫緩，本專案跟進或自行決定）
- [ ] 18 語言 i18n 對 modem 工具是否過重（砍語言可省約 1,500 行，但砍了就難回頭）

## 已完成

- [x] 2026-08-02 **指令盤點報告四批全部執行完畢**（V26.0.23~V26.0.26），詳見
      `reports/at-command-coverage-audit.md`。指令數 61 → 189、頁簽 6 → 9
- [x] 2026-08-02 SSL / HTTP / FTP 三頁簽（V26.0.25~26），98 條指令，零流量 `=?` 逐條驗證
- [x] 2026-08-02 SSL/HTTP/FTP 錯誤碼與 URC 註解（V26.0.26），87 個錯誤碼 + 12 條 URC
- [x] 2026-08-02 **`AT+QWIFISCAN` 結果不回報破案**：不是韌體 bug，是 `AT+QURCCFG="urcport"`
      出廠值為 `usbat`，URC 全送到 USB 埠。切 `uart1` 後立刻掃到 5 個熱點
- [x] 2026-08-02 **`AT+QMTPUBEX` 末參數確認是「長度」不是訊息**（MQTT 應用筆記 §3.3.8），
      已改為兩段式實作；端對端發布仍待真實 broker（併入上面的數據功能實測）
- [x] 2026-08-01 EG800K AT 指令快捷鈕（V26.0.7~V26.0.9）：6 頁簽 61 顆按鈕（Basic 17/GNSS 14/TCP-IP 15/MQTT 11/WiFiScan 4），依官方 PDF 逐條核對 + 實機測試

- [x] 2026-07-31 fork 自 NuMonitor V26.12.0，移除繪圖功能（-2,507 行），瀏覽器實測 + 4 維度稽核通過
- [x] 行尾預設改 CR（AT 指令必需）
- [x] localStorage 鍵改 numodem 前綴
