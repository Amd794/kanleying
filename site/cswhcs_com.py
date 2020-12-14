# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 16:11
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import pyquery

from settings import pc_rules_dict
from threading_download_images import get_response


class Cswhcs(object):
    @staticmethod
    def _cswhcs(pq):
        def is_next_url():
            next_url = ''
            fanye = pq('div.fanye')
            if '下一页' in fanye.text():
                next_url = pyquery.PyQuery(fanye)('a:nth-last-child(2)').attr('href')
            if next_url:
                next_url = 'https://cswhcs.com' + next_url
            else:
                next_url = None
            return next_url

        images_url = []
        next_url = is_next_url()
        while next_url:
            print(next_url)
            if next_url:
                response = get_response(next_url)
                pq = pyquery.PyQuery(response.text)
                divs = pq(pc_rules_dict.get('cswhcs').get('comic_pages'))
                for div in divs:
                    img_src = pyquery.PyQuery(div)('img').attr('data-original')
                    if not img_src:
                        img_src = pyquery.PyQuery(div)('img').attr('src')
                    images_url.append(img_src)
                # 判断是否还有下一页
            next_url = is_next_url()
        return images_url