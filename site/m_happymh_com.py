# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 15:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import re

import execjs

from threading_download_images import get_response


class Happymh(object):
    @staticmethod
    def _happymh(detail_url):
        response = get_response(detail_url)
        ss = re.findall('var ss = ({.*?});', response.text)[0].replace('\\', '')
        ctx = execjs.get().compile(open('js/_m_happymh.js').read(), cwd='js/node_modules')
        data = ctx.call('getArr', eval(ss))
        image_url = [d['url'] for d in data]
        return image_url


if __name__ == '__main__':
    import sys

    sys.path.append('../js')
    print(Happymh._happymh('https://m.happymh.com/manga/read/bailianchengshen/1021588'))
