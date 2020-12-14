# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 15:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import re
import random

import execjs

from threading_download_images import get_response


class PuFei8(object):
    @staticmethod
    def get_images_url(detail_url):
        response = get_response(detail_url)
        packed = re.findall('packed="(.*)";', response.text)[0]
        ctx = execjs.get().compile(open('js/_pufei8.js').read())
        img_urls = ctx.eval(f'getArr("{packed}")')[1:]
        if 'http' in img_urls[0]:
            return img_urls
        if 'taduo' in detail_url:
            img_servers = ["http://mh.jiduo.cc/"]
        else:
            img_servers = ['http://res.img.jituoli.com/', 'http://res.img.fffmanhua.com/']
        images_url = [random.choice(img_servers) + i for i in img_urls]
        return images_url


if __name__ == '__main__':
    # print(PuFei8.get_images_url('http://www.pufei8.com/manhua/1423/138823.html'))
    print(PuFei8.get_images_url('http://www.pufei8.com/manhua/1418/606107.html'))
