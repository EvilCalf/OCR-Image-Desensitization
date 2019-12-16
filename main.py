import os

import cv2
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image, ImageDraw, ImageFont, ImageGrab

tesseract_cmd = r".\tesseract-ocr\tesseract.exe"

for root, dirs, files in os.walk("labimage/"):
    for file in files:
        imgaetype = 1
        image = Image.open(root + "/" + file)
        if image.size[0] == 4032:
            image = image.rotate(-90)
            imgaetype = 2
        content = pytesseract.image_to_data(image, lang="chi_sim12", output_type="dict")
        for i in range(len(content["text"])):
            if 0 < len(content["text"][i]):
                if content["text"][i] == "姓名" or content["text"][i] == "姓" or  content["text"][i] =="名":
                    (x, y, w, h) = (
                        content["left"][i],
                        content["top"][i],
                        content["width"][i],
                        content["height"][i],
                    )
                    print(x, y, w, h)
                    if imgaetype == 1:
                        box = (x - 20, y - 10, x + w + 400, y + h + 30)
                    else:
                        box = (x - 5, y - 5, x + w + 400, y + h + 10)
                    img = image.crop(box)
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
                    elif content["text"][0] != "姓":
                        filename = "./Cache/" + file
                        img.save(filename)
                        img = cv2.imread(filename)
                        content = pytesseract.image_to_string(
                            img, lang="chi_sim12", output_type="dict"
                        )
                    cnt = content["text"]
                    cnt = cnt.replace(" ", "")
                    cnt = cnt[3:]
                    print(cnt)
                    image.paste((0, 0, 0), box)
                    image.save("./Output/" + file)
                    data = pd.DataFrame({"name": [cnt], "dir": [root + "/" + file]})
                    data.to_csv("name2file.csv", mode="a", header=False)
                    break
