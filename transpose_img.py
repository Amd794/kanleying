# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/12/27 21:23
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os

from PIL import Image


def transpose_img(img_path):
    img = Image.open(img_path)
    img = img.transpose(Image.ROTATE_270)  # 将图片旋转270度
    img.save(img_path)


if __name__ == '__main__':
    suffix = ['jpg', 'png', 'jpeg']
    file_list = [imgFileName for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(suffix))]
    file_list.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    print(file_list)
    for file in file_list:
        print(f'--------{file}---------')
        transpose_img(file)

    from shutil import copyfile
    copyfile('C:/Users/29522/Desktop/Project/PyCharm/Python_fullstack/5. 网络爬虫/韩漫/try_to_fix.py',
             os.path.join('./', 'try_to_fix.py'))
    os.system("python try_to_fix.py")
    os.remove(__file__)
