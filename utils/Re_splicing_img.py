# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/30 17:01
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

import hashlib
import os

from PIL import Image, UnidentifiedImageError


def get_num(e, t):
    # 搜索function get_num(e, t)
    n = 10
    mw = hashlib.md5(f'{e}{t}'.encode()).hexdigest()
    if 421925 >= int(e) >= 268850:
        n = ord(mw[-1]) % 10
    elif int(e) >= 421926:
        n = ord(mw[-1]) % 8
    cut_num = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    n = cut_num[n]
    print(n)
    return n


def cut_image(path, filename, photo_id):
    global width, n, item_height
    try:
        image = Image.open(path + filename)
        width, height = image.size
        item_width = width
        print(filename)
        n = get_num(photo_id, str(int(os.path.splitext(os.path.basename(filename))[0]) + 1).rjust(5, '0'))
        # 由上至下切开分成10份
        item_height = height // n
        box_list = []
        to_image = Image.new('RGB', (width, int(item_height * n)))  # 创建一个新图
        for row in range(0, n):
            for col in range(0, 1):
                box = (col * item_width, row * item_height, (col + 1) * item_width, (row + 1) * item_height)
                box_list.append(box)
        for i in range(len(box_list)):
            to_image.paste(image.crop(box_list[::-1][i]), (0, item_height * i))
        to_image.save(path + filename)
    except UnidentifiedImageError as e:
        print(e)
    except SystemError as e:
        Image.new('RGB', (970, 5)).save(path + filename)


if __name__ == '__main__':
    suffix = ['jpg', 'png', 'jpeg']
    file_list = [imgFileName for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(suffix))]
    file_list.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
    print(file_list)
    idss = 1
    for filename in file_list:
        cut_image('./', filename, idss)
    with open('error_urls.txt', 'w') as fw:
        fw.close()
    from shutil import copyfile

    copyfile('C:\\Users\\29522\\Desktop\\Project\\5. 网络爬虫\\韩漫\\try_to_fix.py',
             os.path.join('./', 'try_to_fix.py'))
    os.system("python try_to_fix.py")
    os.remove(__file__)
