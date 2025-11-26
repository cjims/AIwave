# 🏠 智慧 AI 看房系統  
### 2025 雲湧智生：AI 黑客松（DIGITIMES）

本專案為參與 **DIGITIMES 主辦之「2025 雲湧智生：AI 黑客松」競賽成果**，  
結合 **研華（Advantech）ICAM-540 工業級攝影機** 與 **AWS 生成式 AI 服務**，  
打造一套可將實際看屋影像 **即時轉換為多種室內設計風格** 的智慧 AI 看房體驗。

---

## 專案簡介

傳統線上看屋多半僅提供靜態影像或即時影像串流，使用者難以想像未來居住情境。

本專案透過：
-  **ICAM-540 即時影像串流**
-  **AWS 雲端原生架構**
-  **生成式 AI 室內風格轉換（Nova）**
-  **Knowledge Base + RAG 搜尋**

讓使用者能夠直觀地看到「同一空間的不同風格樣貌」，提升看屋與決策體驗。

---

## 技術亮點

- **Multi-Modal AI**：結合影像 + 文字的生成式模型應用  
- **Reasoning LLM**：透過 Knowledge Base 提供語意理解與查詢  
- **Cloud-Native 架構**：Lambda + S3 + Bedrock  
- 即時影像到生成內容的串接流程

---

## 系統架構
<p align="center">
  <img src="https://raw.githubusercontent.com/cjims/AIwave/main/pic/Framework1.png" width="720">
</p>

系統主要分為四個模組：

| 模組 | 說明 |
|----|----|
| AWS Lambda | 影像處理、串流轉檔、S3 存取 |
| Knowledge Base | 建立 RAG 搜尋與 API |
| Generative AI | Nova 模型進行室內風格轉換 |
| Frontend | 使用者操作與成果展示 |

---

## AWS Lambda

### 環境需求
- 需安裝 **FFmpeg**

### 功能檔案

| 檔案名稱 | 功能 |
|--------|------|
| `myLambdaFunction.py` | 將 Kinesis Video Stream 影像即時串流並儲存至 S3 |
| `getPictures.py` | 列出 S3 中的圖片供前端取得 |
| `getNovaGenPictures.py` | 產生已生成影像 / 影片的存取連結 |

---

## Knowledge Base（RAG）

將 S3 內的資料建立為 Knowledge Base，並透過 **Bedrock Agent API** 提供給前端查詢。

```bash
python data_automation.py
```

## Nova生成模組（Nova-Gen）

本專案使用 AWS Bedrock Nova 系列模型 進行影像生成與風格轉換。

1. 各nova_*.py對應不同模型
2. 不同模型帶入的參數與生成風格不同
3. 可擴充更多室內設計風格主題

## Frontend

```bash
python3 -m http.server 8080
```

點開index.html

<p align="center">
<img src="https://github.com/cjims/AIwave/blob/main/pic/front1.png" width="600">
</p>

<p align="center">
<img src="https://github.com/cjims/AIwave/blob/main/pic/front2.png" width="600">
</p>

## Demo

<p align="center">原始影像</p>

<p align="center">
<img src="https://github.com/cjims/AIwave/blob/main/pic/521793.jpg" width="500", >
</p>

<p align="center">AI 生成：現代極簡風青年旅宿</p>

<p align="center">
<img src="https://github.com/cjims/AIwave/blob/main/pic/521793_designed.jpg" width="500">
</p>
