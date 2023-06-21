# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/4/12 13:39
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os

from PIL import Image


def make_pdf(pdf_name: 'int(name).jpg|png|gif|jpeg', file_list):
    im_list = []

    im1 = Image.open(file_list[0])
    file_list.pop(0)
    for i in file_list:
        img = Image.open(i)
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)


if __name__ == '__main__':
    current_work_path = f'{os.path.abspath(os.path.dirname(os.path.abspath(__file__)))}'
    dir_list = os.listdir(current_work_path)
    dir_list.pop(dir_list.index(os.path.basename(__file__)))
    for i in dir_list:
        os.chdir(i)
        print(os.getcwd())
        file_name = ''
        suffix = ['jpg', 'png', 'gif', 'jpeg']
        file_list = ['./' + str(imgFileName) for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(suffix))]
        file_list.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))
        # print(file_list)
        for imgFileName in os.listdir('.'):
            if imgFileName.endswith('pdf'):
                file_name = (os.path.splitext(imgFileName)[0])
        make_pdf('重构-' + file_name + '.pdf', file_list)
        os.remove(file_name + '.pdf')
        print('重构-' + file_name + '.pdf' + '---->successful')
        os.chdir(current_work_path)
