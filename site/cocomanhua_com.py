# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 15:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

import re

import execjs

from threading_download_images import get_response


class CoCoManHua(object):
    @staticmethod
    def _cocomanhua(detail_url):
        response = get_response(detail_url)
        data = re.findall('var C_DATA.*?\'(.*?)\'', response.text)[0]
        ctx = execjs.get().compile(open('js/_cocomanhua.js', encoding='utf-8').read(), cwd='js/node_modules')
        images_url = ctx.eval(f'getArr("{data}")')
        return images_url


if __name__ == '__main__':
    print(CoCoManHua._cocomanhua('https://www.cocomanhua.com/11701/1/188.html'))
