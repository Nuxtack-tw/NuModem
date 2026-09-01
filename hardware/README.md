# hardware/ —— NuCom-EG800u 載板

`NuModem_EG800.html` 是對著這塊自製載板開發與驗證的。
**不用這塊板子也能用該工具**（任何能接上 EG800K 的 USB/UART 轉接都行），
但說明書與 `reports/` 裡的實測數據都出自它。

| 檔案 | 內容 |
|---|---|
| `NuCom-EG800u-V0.2a.pdf` | 電路圖（V0.2a，2026-09-01） |
| `NuCom-EG800u-V0.2.png` | 實體照片，正反面（**V0.2**，比電路圖早一個小改版） |

規格摘要與「為什麼 RTS 是電源、DTR 是 Reset」的硬體成因，見專案根目錄
[`README.md`](../README.md) 的〈搭配的硬體〉一節。

## 授權：CC BY-SA 4.0

本目錄的內容採 **[Creative Commons 姓名標示-相同方式分享 4.0 國際](https://creativecommons.org/licenses/by-sa/4.0/)**
（CC BY-SA 4.0），完整條文見專案根目錄的 [`LICENSE-CC-BY-SA-4.0.txt`](../LICENSE-CC-BY-SA-4.0.txt)。

⚠ **與專案其餘部分不同**：程式碼、說明書、報告、翻譯採 MIT；
**只有這個目錄採 CC BY-SA 4.0**。原因是 MIT 的條文寫的是「the Software」，
套在電路圖上並不精準；硬體設計慣用 CC BY-SA 或 CERN-OHL。

實務上這代表：

- ✅ 可自由使用、修改、重製、散布，**含商業用途**
- ✅ 可據此打板、改版、做成自己的產品
- ⚠ 必須**標示原作者**並指明是否有修改
- ⚠ **相同方式分享**：若散布改作後的電路圖，該改作也必須採 CC BY-SA 4.0
  （這一條 MIT 沒有 —— 拿去改的人有回饋義務）

> 註：ShareAlike 的義務落在**電路圖這個作品本身**的散布。
> 依此設計製造的實體板子不因此受 copyleft 約束 ——
> CC 授權管的是著作權，不是專利或製造行為。

## 這不是移遠的參考設計

本電路圖為自行設計（`NX-NuCom-EG800u`），與 Quectel 官方的
hardware design／reference design 是不同的東西。
移遠的文件受其版權與保密條款拘束、不隨本專案發佈，詳見
[`NOTICE.md`](../NOTICE.md) §1。
