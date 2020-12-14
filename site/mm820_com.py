# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 16:35
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import pyquery

from settings import pc_rules_dict
from threading_download_images import get_response


class Mm820(object):
    # 该站点进行了分页处理, 需要特殊处理
    @staticmethod
    def _mm820(detail_url, pages: int):
        images_url = []
        for i in range(2, pages + 1):
            response = get_response(detail_url + f'?page={i}')
            pq = pyquery.PyQuery(response.text)
            divs = pq(pc_rules_dict.get('mm820').get('comic_pages'))
            for div in divs:
                img_src = pyquery.PyQuery(div)('img').attr('data-original')
                if not img_src:
                    img_src = pyquery.PyQuery(div)('img').attr('src')
                images_url.append(img_src)
        return images_url
