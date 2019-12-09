# OCR 脱敏工具DEMO

* 采用了Tesseract-Ocr模块，使用的LSTM模型进行训练。

* 可以识别图片中的姓名，并把相关区域填充(0,0,0)像素点，并将获取的姓名与文件目录保存到CSV中。

* 将需要脱敏的图片放入labimage中，python main.py，即可批量脱敏操作。
