# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/11/22 19:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os
import re
from shutil import copyfile

from PIL import Image

# os.chdir(r'C:\Users\29522\Desktop\Project\PyCharm\Python_fullstack\5. 网络爬虫\韩漫\kanleying\闯入我们家的H先生\第 33 话')


def f(s):
    try:
        return int(re.findall('\d+', s)[0])
    except IndexError:
        return 999


suffix = ['jpg', 'png', 'jpeg']
page = 5
file_list = [imgFileName for imgFileName in os.listdir('.') if
             imgFileName.endswith(tuple(suffix))]
file_list.sort(key=f)
file_groups = [[x for x in file_list][i:i + page] for i in range(0, len(file_list), page)]
file_name = ''
for group in file_groups:
    print(f'-----正在操作{group}分组-----')
    image = Image.open(group[0])
    width, height = image.size
    to_image = Image.new('RGB', (width * page, height))  # 创建一个新图
    for pic in group:
        file_name = pic.replace('_w_144', '')
        # 从左到右粘贴图片
        to_image.paste(Image.open(pic), (int(width) * group.index(pic), 0))
    to_image.save(file_name)
    # 及时释放文件
    image.close()
    to_image.close()
for i in file_list:
    try:
        os.remove(i)
        print()
    except PermissionError:
        print(f'-----{i} PermissionError-----')

with open('error_urls.txt', 'w') as fw:
    fw.close()

copyfile(r'C:\Users\29522\Desktop\Project\5. 网络爬虫/韩漫/try_to_fix.py',
         os.path.join('./', 'try_to_fix.py'))
os.system("python try_to_fix.py")
os.remove(__file__)
