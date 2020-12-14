# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 15:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import re

import execjs

from threading_download_images import get_response


class AcQq(object):
    @staticmethod
    def _ac_qq(detail_url):
        # 如果需要配置cookie请按下面配置
        # headers = {
        #     'cookie':
        # }
        response = get_response(detail_url)
        N = re.findall('window\["n.*?e"\]\s=\s(.*?);', response.text)[1]
        T = re.findall('var DATA.*?\'(.*?)\'', response.text)[0]
        ctx = execjs.get().compile(open('js/_ac_qq.js', encoding='gbk').read(), cwd='js/node_modules')
        data = ctx.call('getArr', T, N)
        images_url = [picture['url'] for picture in data['picture']]
        return images_url


if __name__ == '__main__':
    import sys

    sys.path.append('../js')
    print(AcQq._ac_qq('https://ac.qq.com/ComicView/index/id/635142/cid/193'))
