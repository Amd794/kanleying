# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/11/19 13:51
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os

import cv2
import numpy as np
from PIL import Image


def watermark(path, newPath):
    img = cv2.imread(path, 1)
    hight, width, depth = img.shape[0:3]

    # 截取 右下角
    cropped = img[int(hight * 0.91):hight, int(width * 0.7):width]  # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imwrite(newPath, cropped)
    imgSY = cv2.imread(newPath, 1)

    # 图片二值化处理，把[200,200,200]-[250,250,250]以外的颜色变成0
    thresh = cv2.inRange(imgSY, np.array([200, 200, 200]), np.array([250, 250, 250]))
    # 创建形状和尺寸的结构元素
    kernel = np.ones((5, 5), np.uint8)
    # 扩展待修复区域
    hi_mask = cv2.dilate(thresh, kernel, iterations=10)
    specular = cv2.inpaint(imgSY, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    cv2.imwrite(newPath, specular)

    # 覆盖图片
    imgSY = Image.open(newPath)
    img = Image.open(path)
    img.paste(imgSY, (int(width * 0.7), int(hight * 0.91), width, hight))
    img.save(newPath)


if __name__ == '__main__':
    dir = os.chdir(
        r'C:\Users\29522\Desktop\Project\PyCharm\Python_fullstack\5. 网络爬虫\韩漫\kanleying\我的九尾狐女友\第10话 Chapter10 2019-06-28')
    print(dir)
    path = "49.jpg"
    newPath = "new.jpg"
    for i in range(51):
        path = f"{i}.jpg"
        newPath = f"{i}.jpg"
        watermark(path, newPath)
