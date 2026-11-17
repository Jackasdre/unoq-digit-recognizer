# UNO Q 手寫數字辨識（Edge AI on Arduino UNO Q）

在 Arduino UNO Q 上即時辨識手寫數字：在手機或電腦的網頁上寫一個 0–9 的數字，板子在**本地**用自己訓練的 CNN 推論，結果顯示在板載的 **8×13 LED 矩陣**上。不需要任何外接零件，資料也不上雲。

## 系統架構

```
瀏覽器（手寫畫布）
   │  前處理：裁切 → 縮放 20×20 → 置中 28×28 → 784 個像素值
   ▼  HTTP POST /predict
UNO Q Linux 端（Qualcomm QRB2210, Debian）
   │  WebUI Brick + ONNX Runtime 推論（DigitCNN）
   ▼  Bridge.call("draw", frame)
UNO Q MCU 端（STM32U585）
      Arduino_LED_Matrix：左邊顯示數字，右邊光柱顯示信心
```

## 模型

- 以 PyTorch 在 MNIST 上訓練（見 `training/`），匯出為 ONNX 部署到板子
- 架構：Conv(1→16) → Pool → Conv(16→32) → Pool → FC(1568→128) → Dropout → FC(128→10)
- 資料增強：隨機旋轉 ±10°、平移 10%、縮放 0.8–1.2，讓模型能適應網頁手寫
- 模型大小約 820 KB

## 成果

| 項目 | 結果 |
|---|---|
| MNIST 測試集準確率 | 99.06% |
| PyTorch vs ONNX 輸出差異 | 最大 1.9×10⁻⁶ |
| UNO Q 單張推論時間 | 約 1.3 ms |

## 檔案說明

```
app.yaml                  App Lab 設定（使用 web_ui brick）
assets/index.html         手寫網頁與前處理
python/main.py            Linux 端主程式：API、推論、透過 Bridge 傳給 MCU
python/digit_model.py     ONNX Runtime 推論
python/matrix_display.py  將結果轉成 8×13 LED 矩陣畫面（5×7 數字字型 + 信心光柱）
python/digit_cnn.onnx     訓練好的模型
sketch/sketch.ino         MCU 端：接收畫面並顯示在 LED 矩陣
training/                 Colab 訓練筆記本（PyTorch）
```

## 執行方式

1. 將整個資料夾放到 UNO Q 的 `~/ArduinoApps/` 下
2. 在 Arduino App Lab 的 My Apps 開啟 **Digit Recognizer**，按 Run
3. 用同網路的瀏覽器開啟 `http://<板子IP>:7000`
