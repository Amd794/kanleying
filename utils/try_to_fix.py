# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/3/30 23:49
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

import os
import platform as pf
import re
import subprocess

import requests
from PIL import Image, ImageFont, ImageDraw

requests.packages.urllib3.disable_warnings()


def create_img(text, img_save_path):
    font_size = 24
    liens = text.split('\n')
    im = Image.new("RGB", (len(text) * 12, len(liens) * (font_size + 5)), '#fff')
    dr = ImageDraw.Draw(im)
    font_path = r"C:\Windows\Fonts\STKAITI.TTF"
    font = ImageFont.truetype(font_path, font_size)
    dr.text((0, 0), text, font=font, fill="blue")
    im.save(img_save_path)


def make_pdf(pdf_name, file_list):
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


def get_response(url: str, max_count: int = 3, timeout: int = 25,
                 encoding: str = 'utf-8', name: str = '', ) -> object:
    if 'qinqinmh' in url:
        referer = 'https://www.qinqinmh.com/'
    else:
        referer = url
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36 Edg/87.0.664.47',

        'referer': referer,
        # 不缓存
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
    }
    count = 0
    while count < max_count:
        try:
            response = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
            response.raise_for_status()  # 如果status_code不是200,产生异常requests.HTTPError
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException:
            print(f'\033[22;33;m{url} {name}连接超时, 正在进行第{count + 1}次连接重试, {timeout}秒超时重连\033[m')
            count += 1
    else:
        print(f'\033[22;31;m{url}重试{max_count}次后依然连接失败, 放弃连接...\033[m')
        return None


def try_download_error_img(error_file):
    fail_url = []
    with open(error_file) as f:
        images_url = f.read().split('\n')
        images_url = [i for i in images_url if i != '']
    for image_url in images_url:
        image_url, name = image_url.rsplit(' ', 1)

        response = get_response(image_url, timeout=60)
        with open(name, 'wb') as f:
            if response:
                f.write(response.content)
                print(f'成功{image_url}-{name}')
            else:
                f.close()
                fail_url.append(image_url + ' ' + name + '\n')
                print(f'失败{image_url}-{name}')
                create_img(f'温馨提示{image_url}-{name}已经失效', name)
    if fail_url:
        with open(error_file, 'w') as f:
            f.write(''.join(fail_url))
    else:
        print('全部完成')
        os.remove(error_file)
        os.remove(__file__)


def compress(target, source, pwd='', delete_source=False, ):
    """
        压缩加密，并删除原数据
        window系统调用rar程序

        linux等其他系统调用内置命令 zip -P123 tar source
        默认不删除原文件
    """
    if pwd: pwd = '-p' + pwd
    if pf.system() == "Windows":
        cmd = f'rar a {pwd} {target} {source} -x*.rar -x*.py'
        p = subprocess.Popen(cmd, executable=r'D:/Sorfwares/WinRAR/WinRAR.exe')
        p.wait()
    else:
        cmd = f'zip a {pwd} {target} {source} -x*.rar -x*.py'
        p = subprocess.Popen(cmd)
        p.wait()
        # os.system(" ".join(cmd))
    if delete_source:
        os.remove(source)


def f(sl):
    try:
        return list(map(int, re.findall('(\d+)', sl)))
    except IndexError:
        if '最终' in sl:
            return 888
        elif '后记' in sl:
            return 999
        elif '序章' in sl:
            return -1
        elif 'Preview' in sl:
            return -2
        return 999


if __name__ == '__main__':
    error_file = 'error_urls.txt'
    # 判断该路径是否存在某文件
    if not os.access(error_file, os.F_OK):
        print(f'-----{error_file}不存在------')
        with open(error_file, 'w') as fw:
            fw.close()
    file_name = ''
    for imgFileName in os.listdir('.'):
        if imgFileName.endswith('pdf'):
            file_name = (os.path.splitext(imgFileName)[0])
    # 不存在pdf文件则重新命名
    if not file_name:
        base_dir = os.getcwd()
        chapter = os.path.split(base_dir)[1]
        comic = os.path.split(os.path.split(base_dir)[0])[1]
        file_name = f'{comic}-{chapter}'
    print(f'当前正常尝试修复---->{file_name}')
    try_download_error_img(error_file)

    suffix = ['jpg', 'png', 'gif', 'jpeg']
    file_list = ['./' + str(imgFileName) for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(suffix))]
    file_list.sort(key=f)
    print(file_list)
    if ['./' + str(imgFileName) for imgFileName in os.listdir('.') if imgFileName.endswith(tuple(['.pdf']))]:
        make_pdf(file_name + '.pdf', file_list)
        print(file_name + '-重构' + '.pdf' + '---->successful')
        # compress(f'{file_name}.rar', '*', file_name)
