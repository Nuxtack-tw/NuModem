# 版權與第三方元件聲明

> 最後更新：2026-09-01

本檔說明 NuModem EG800 的內容來源、對第三方素材的處理方式，以及執行期依賴的外部資源。

---

## §1 本專案**不含**任何 Quectel（移遠通信）文件

開發過程參考了 Quectel 官方的 AT 指令手冊與應用筆記，但**這些 PDF 一律不隨本專案發佈**。

原因不是體積，是授權。這些文件本身載明（三種模板措辭略異，限制一致）：

| 文件 | 條文節錄 |
|---|---|
| AT Commands Manual v1.4 | 「shall not be copied, reproduced, **distributed**, merged, **published**, translated, or modified **without prior written consent**」 |
| SSL／GNSS 等應用筆記 | 「you shall not ... copy, reproduce, **republish**, display, translate, **distribute** ... or create derivative works」 |
| QuecLocator AN（舊版模板） | 「**DISSEMINATION** ... **ARE FORBIDDEN WITHOUT PERMISSION. OFFENDERS WILL BE HELD LIABLE FOR PAYMENT OF DAMAGES.**」 |

多數文件另附**保密義務**（「shall be kept confidential, unless expressly authorized」）——
限制的是揭露行為本身，比單純的重製權更嚴。

**需要這些文件請自行向 Quectel 取得**：<https://www.quectel.com/> 的下載專區，
或聯繫你的 FAE／代理商。

## §2 引用方式

本專案的文件與報告在引用 Quectel 資料時遵守以下原則：

- **只標書目資訊**：冊名、版本、章節、頁碼 —— 這些是事實，不受著作權保護
- **引述限於必要範圍**並註明出處（依著作權法第 52 條之引用、第 65 條之合理使用）
- **不重製表格或章節全文**，不提供文件本身的副本或連結轉載

⚠ 版本號一律以 **PDF 內文**為準，不以檔名為準 —— 移遠的檔名版本經常落後於內文版本。

## §3 實測內容為原創

說明書（`doc/manual.html`）與 `reports/` 底下的內容，
來自 2026 年 7–9 月對實體 EG800K（韌體 `EG800KCNGCR07A06M04`）的實際操作與量測，
**不是手冊的改寫或翻譯**。手冊與實機行為不符之處，文中直接指出並以實測為準
（例如 `AT+QGPSDEL` 是半實作殘根、Wi-Fi Scan 的參數範圍文件放寬但韌體未放寬）。

AT 指令名稱與語法屬功能性、事實性表達，使用它們不構成對文件的重製。

## §4 執行期的第三方資源

主程式是單一 HTML 檔，**不打包任何第三方程式碼**；以下資源在執行期由瀏覽器取得。

| 資源 | 用途 | 授權／條款 | 何時載入 |
|---|---|---|---|
| **Leaflet 1.9.4**（cdnjs） | 地圖頁的圖台 | BSD-2-Clause | 延遲載入 —— 只有切到地圖頁才抓 |
| **OpenStreetMap 磚圖**<br>`tile.openstreetmap.org` | 地圖底圖 | 圖資 **ODbL 1.0**；磚圖圖像 **CC BY-SA 2.0**。程式已內建署名字串（`NuModem_EG800.html` 的 `tileLayer` attribution） | 同上 |
| **Google Fonts** | `JetBrains Mono`、`Space Grotesk` | 兩者皆 SIL OFL 1.1 | 開啟頁面時 |
| **flagcdn.com** | 語言選單的 37 面國旗圖示（`w20/<國碼>.png`） | 熱連結，未重製；**條款請自行向 flagcdn 確認** | 開啟語言選單時 |

### 關於 OSM 磚圖

`tile.openstreetmap.org` 有[磚圖使用政策](https://operations.osmfoundation.org/policies/tiles/)，
禁止大量下載與高頻請求。本工具屬個人、低頻使用；
**若要改作商用或大量部署，請自備磚圖伺服器或改用商業圖磚供應商。**

說明書的 `doc/img/21-map-track.png` 含 OSM 衍生的地圖影像，
該圖已保留 Leaflet 與 OpenStreetMap 的署名（依 ODbL 的姓名標示要求，
即使該圖其餘部分經過模糊化處理，署名區塊仍維持清晰可辨）。

## §5 離線行為

拔掉網路時：地圖頁與國旗圖示不可用，字型退回系統預設，**其餘功能完全正常** ——
序列埠通訊、AT 指令面板、終端機、18 語言介面都不依賴網路。
`js/i18n/` 是本機檔案，不是 CDN。

## §6 本專案自身的授權：軟體 MIT ＋ 硬體 CC BY-SA 4.0

Copyright (c) 2026 Nuxtack。**依內容型態分成兩種授權**：

| 範圍 | 授權 | 條文 |
|---|---|---|
| 主程式 `NuModem_EG800.html`、`js/i18n/` 翻譯檔、`doc/` 的 18 語說明書與截圖、`reports/` 實測報告、`tools/` 腳本 | **MIT** | [`LICENSE`](LICENSE) |
| **`hardware/`** —— 自製載板電路圖 | **CC BY-SA 4.0** | [`LICENSE-CC-BY-SA-4.0.txt`](LICENSE-CC-BY-SA-4.0.txt) |

**為什麼分開**：MIT 的條文寫的是「the Software」，套在電路圖上並不精準；
硬體設計慣用 CC BY-SA 或 CERN-OHL。分開授權才對得上各自的性質。

**兩者的實質差別**：MIT 只要求保留版權聲明；
CC BY-SA 多了 **ShareAlike** —— 散布改作後的電路圖時，該改作也必須採 CC BY-SA 4.0。
拿去改的人有回饋義務，MIT 沒有這條。

> ShareAlike 的義務落在**電路圖這個作品**的散布上。
> 依此設計製造的實體板子不受 copyleft 約束 —— CC 授權管著作權，不管專利或製造行為。

細節見 [`hardware/README.md`](hardware/README.md)。

**不涵蓋**：

| 項目 | 適用條款 |
|---|---|
| Quectel 的文件內容 | 本專案未包含（§1）；引用部分屬合理使用，不因 MIT 而轉為可自由散布 |
| Leaflet、Google Fonts | 各自的 BSD-2-Clause／OFL 1.1（§4） |
| OpenStreetMap 磚圖與圖資 | ODbL 1.0／CC BY-SA 2.0（§4）—— **含 `doc/img/21-map-track.png`** |
| flagcdn 的國旗圖 | 熱連結，未重製；條款見 flagcdn |

換句話說：**MIT 授權的是「我們寫的東西」，不是「我們引用或連結的東西」。**
fork 本專案時，第三方素材的義務照樣要遵守。

---

## §7 相關文件

| 檔案 | 內容 |
|---|---|
| `README.md` | 專案說明與使用方式 |
| `reports/appnote-coverage-final-audit.md` | 應用手冊逐冊覆蓋分析（只引書目資訊） |
| `CLAUDE.md` | 參考資料的存放位置與引用規則（開發者向） |
