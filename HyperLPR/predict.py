import importlib
import sys
import time
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import HyperLPRLite as pr

importlib.reload(sys)

fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0)


def drawRectBox(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])),
                  (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                  (0, 0, 255), 2, cv2.LINE_AA)

    cv2.rectangle(image, (int(rect[0] - 1), int(rect[1]) - 16),
                  (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
                  cv2.LINE_AA)

    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text(
        (int(rect[0] + 1), int(rect[1] - 16)),
        addText, (255, 255, 255),
        font=fontC)
    imagex = np.array(img)
    return imagex


import os


def cutimage(dir):
    correct = 0
    tt = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root, file)
            turename = os.path.splitext(file)[0]
            
            image = cv2.imread(filepath)  #opencv剪切图片
            for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(
                    image):

                image = drawRectBox(image, rect,
                                    pstr + " " + str(round(confidence, 3)))
                print("真实车牌为：", turename)
                print("识别车牌为:", pstr)
                if turename[0]==pstr[0] and turename[1]==pstr[1]\
                    and turename[2]==pstr[2] and turename[3]==pstr[3]\
                    and turename[4]==pstr[4] and turename[5]==pstr[5]\
                    and turename[6]==pstr[6]:
                    correct += 1
                    print("预测正确")
                tt += 1
                print("置信值", confidence)
    return correct, tt       

if __name__ == '__main__':
    startime = time.time()
    
    dir = "./images_rec"
    model = pr.LPR("model/cascade.xml", "model/model12.h5",
                           "model/ocr_plate_all_gru.h5")
    correct, tt = cutimage(dir)
    usetime = time.time() - startime
    print("共有{}张图片参与测试，预测正确{}张\n程序运行时间时间：{}s\
            \n准确率：{}%\n平均每幅图片耗时：{}s".format(
            tt,
            correct,
            usetime,
            (correct/tt*100),
            (usetime/tt)
            )
        )
   