import os

import cv2
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image, ImageDraw, ImageFont, ImageGrab

tesseract_cmd = r".\tesseract-ocr\tesseract.exe"

for root, dirs, files in os.walk("labimage/"):
    for file in files:
        image = Image.open(root + "/" + file)
        content = pytesseract.image_to_data(image, lang="chi_sim43", output_type="dict")
        for i in range(len(content["text"])):
            if 0 < len(content["text"][i]):
                if content["text"][i] == "姓名" or (
                    content["text"][i] == "姓" and content["text"][i + 1] == "名"
                ):
                    (x, y, w, h) = (
                        content["left"][i],
                        content["top"][i],
                        content["width"][i],
                        content["height"][i],
                    )
                    print(x, y, w, h)
                    img = image.crop((x - 10, y - 10, x + w + 400, y + h + 30))
                    content = pytesseract.image_to_string(
                        img, lang="chi_sim43", output_type="dict"
                    )
                    if content["text"] == "":
                        filename = "./Cache/" + file
                        img.save(filename)
                        img = cv2.imread(filename)
                        content = pytesseract.image_to_string(
                            img, lang="chi_sim43", output_type="dict"
                        )
                    cnt = content["text"]
                    cnt = cnt.replace(" ", "")
                    cnt = cnt[3:]
                    print(cnt)
                    image.paste((0, 0, 0), (x - 10, y - 10, x + w + 400, y + h + 30))
                    image.save("./Output/" + file)
                    data = pd.DataFrame({"name": [cnt], "dir": [root + "/" + file]})
                    data.to_csv("name2file.csv", mode="a", header=False)
                    break
