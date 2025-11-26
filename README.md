# 2025雲湧智生:AI黑客松

## Abstract

此專案為參與由DIGITIMES主辦的競賽，競賽內容為雲端基礎設施的生成式AI服務(AWS服務)，並透過培訓工作坊，協助參賽團隊建構**多代理協作(Multi-agent collaboration)**、**多模態AI模型(Multi-modal AI Models)**、**具備推理能力的大型語言模型 (Reasoning LLM)**等技術，期望參賽者在完善且擁有安全架構及數據資料的開發環境中，提出創新應用與打造現場展示成果。

因部屬在雲端，因此當中會分成好幾個部分: Lambda、Fronted、Knowledge_base、生成影像程式。

## Architecture
![images]()
環境做法 : <br>

先校正WSL2驅動，接著再安裝usbipd，最後接上XLaunch，進行錄影畫面的顯示，有可能會因為網路有一些小延遲，按下確認後須注意。

程式流程 : <br>

程式啟動，對準人臉後，按下enter進行截圖，圖片會存到face_id的資料夾中，抓取到的特徵點會存到DB進去，最後再傳回程式辨識是誰。
如果想重複寫入，需要重新再按下enter確認，名字打的跟之前的一樣，DB的特徵就會被覆蓋過去。

</details>

## Getting started(windows)
1. 確保[環境](https://blog.csdn.net/qq_40087136/article/details/145190221)已經都OK
2. 在使用XLanch時，需注意WSL環境是否有設定lanch的環境IP變數
3. `usb IP.txt`可以參考
4. install.sh已經幫你建好虛擬環境以及所需套件，必要時也可以參考`requirements.txt`

### Install
```
chmod +x install.sh
./install.sh
```

## Getting started(Linux)

### Install
```
chmod +x install.sh
./install.sh
```

## DB
部門是利用Postgresql，資料庫參數的調整在`db_config.env`

## 啟動
要先安裝`v4l2-ctl`，查看USB cam能夠支援到裝置的何種解析度，視情況將相對應的數值填入程式中
```
v4l2-ctl -d /dev/video0 --list-formats-ext
```
主要辨識程式在`get_cam_name.py`，參數調整在`main.py`
```
python3 main.py
```

## 使用範例

https://github.com/user-attachments/assets/4843eaeb-3589-409e-93f1-7615f4095022

