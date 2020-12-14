# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 15:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import re

import execjs

from threading_download_images import get_response


class Momomh(object):
    @staticmethod
    def _momomh(detail_url):
        header = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/85.0.4183.83',
        }
        response = get_response(detail_url, header=header)
        load_conf = re.findall('loadConf    =  ({.*?})', response.text, re.S)[0].strip('\n')
        word = ['i:', 'c:', 'k:', 'd:', 'l:', 'f:']
        for i in word:
            load_conf = load_conf.replace(i, l := f'"{i[0]}":')
        ctx = execjs.get().compile(open('js/_momomh.js').read(), cwd='js/node_modules')
        data = ctx.call('getArr', eval(load_conf))
        image_url = [url.strip('_w_720') for url in data]
        return image_url


if __name__ == '__main__':
    from pathlib import Path
    import os
    dir = Path().absolute().parent
    os.chdir(dir)
    print(Momomh._momomh('https://m.momomh.com/view/Y6dW9.html'))
    print(Momomh._momomh('https://m.momomh.com/view/NppbB.html'))
