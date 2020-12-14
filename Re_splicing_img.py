# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/30 17:01
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

import os

from PIL import Image


def cut_image(path, filename):
    image = Image.open(path + filename)
    width, height = image.size
    to_image = Image.new('RGB', (width, height))  # 创建一个新图
    item_width = width
    # 由上至下切开分成10份
    item_height = height // 10
    box_list = []
    for row in range(0, 10):
        for col in range(0, 1):
            box = (col * item_width, row * item_height, (col + 1) * item_width, (row + 1) * item_height)
            box_list.append(box)
    for i in range(len(box_list)):
        to_image.paste(image.crop(box_list[::-1][i]), (0, int(item_height) * i))
    to_image.save(path + filename)


if __name__ == '__main__':
    suffix = ['jpg', 'png', 'jpeg']
    file_list = [imgFileName for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(suffix))]
    file_list.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    print(file_list)
    for filename in file_list:
        cut_image('./', filename)
    with open('error_urls.txt', 'w') as fw:
        fw.close()
    from shutil import copyfile

    copyfile('C:/Users/29522/Desktop/Project/PyCharm/Python_fullstack/5. 网络爬虫/韩漫/try_to_fix.py',
             os.path.join('./', 'try_to_fix.py'))
    os.system("python try_to_fix.py")
    os.remove(__file__)
