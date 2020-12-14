# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/3/28 19:22
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


import os, re
import threading

import requests
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()
glock = threading.Lock()


#   todo 获取返回的response
def get_response(url: str, error_file_path: str = '.', max_count: int = 3, timeout: int = 25,
                 encoding: str = 'utf-8', name: str = '', header: dict = {}) -> object:
    ua = UserAgent()
    if not header:
        headers = {
            'User-Agent': getattr(ua, 'random'),
            'referer': url,
        }
    else:
        headers = header
    count = 0
    while count < max_count:
        try:
            response = requests.get(url=url, headers=headers, verify=True, timeout=timeout, )
            response.raise_for_status()  # 如果status_code不是200,产生异常requests.HTTPError
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException:
            print(f'\033[22;33;m{url} {name}连接超时, 正在进行第{count + 1}次连接重试, {timeout}秒超时重连\033[m')
            count += 1
    else:
        print(f'\033[22;31;m{url}重试{max_count}次后依然连接失败, 放弃连接...\033[m')
        if not os.path.exists(error_file_path):
            os.makedirs(error_file_path)
        glock.acquire()
        with open(os.path.join(error_file_path, 'error_urls.txt'), 'a') as f:
            f.write(url + ' ' + name + '\n')
        glock.release()
        return None


# todo 多线程
def thread_run(threads_num, target, args: tuple):
    threads = []
    for _ in range(threads_num):
        t = threading.Thread(target=target, args=args)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


# todo 下载图片
def download_images(file_path, images: list, headers):
    from PIL import Image, ImageFont, ImageDraw

    def create_img(text, img_save_path):
        font_size = 24
        liens = text.split('\n')
        im = Image.new("RGB", (len(text) * 12, len(liens) * (font_size + 5)), '#fff')
        dr = ImageDraw.Draw(im)
        font_path = r"C:\Windows\Fonts\STKAITI.TTF"
        font = ImageFont.truetype(font_path, font_size)
        dr.text((0, 0), text, font=font, fill="blue")
        im.save(img_save_path)

    while images:
        glock.acquire()
        try:
            image_url = images.pop()
        except IndexError:
            print('**************IndexError******************')
        if '18comic3' in image_url:
            image_url = image_url.replace('18comic3', '18comic4')
            print('***************18comic3*****************')

        file_name = str(len(images)) + '.jpg'
        # 处理一下momomh链接
        if '_w_' in image_url:
            file_name = str(len(images)) + '_w_144.jpg'
            image_url = re.sub('_w_\d+', '', image_url)
        print(f'{threading.current_thread()}:正在下载{file_name} ---> {image_url}')
        glock.release()
        response = get_response(image_url, file_path, name=file_name, header=headers)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(os.path.join(file_path, file_name), 'wb') as f:
            if response:
                f.write(response.content)
            else:
                f.close()
                create_img(f'温馨提示{image_url}已经失效', os.path.join(file_path, file_name))

    if 'error_urls.txt' in os.listdir(file_path):
        from shutil import copyfile
        copyfile('./try_to_fix.py', os.path.join(file_path, 'try_to_fix.py'))


def download(image_list: list, file_path=os.getcwd(), threads_num=5, headers={}, ):
    thread_run(threads_num, download_images, (file_path, image_list, headers))


if __name__ == '__main__':
    imgs = [
        'http://res.img.jituoli.com/images/2020/09/21/11/51d97a4d0b.jpg/0',
        'http://res.img.fffmanhua.com/images/2020/09/21/11/51d97a4d0b.jpg/0',
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
        # 'Referer': 'http://www.manhuatai.com/cjtksdcz/xz.html?from=kmhapp',
    }
    download(imgs, f'./{os.path.basename(__file__).strip(".py")}/test/', 2)
