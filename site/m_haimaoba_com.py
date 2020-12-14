# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 16:26
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import pyquery

from settings import pc_rules_dict
from threading_download_images import get_response


class HaiMaoBa(object):
    @staticmethod
    def _haimaoba(detail_url):

        images_url = []

        def get_one_page_img(detail_url):
            response = get_response(detail_url)
            pq = pyquery.PyQuery(response.text)
            divs = pq(pc_rules_dict.get('haimaoba').get('comic_pages'))
            for div in divs:
                img_src = pyquery.PyQuery(div)('img').attr('src')
                images_url.append(img_src)
            fanye = pq('.fanye1 a')
            if fanye:
                next_url = pyquery.PyQuery(fanye).attr('href')
                next_url = 'http://m.haimaoba.com' + next_url
            else:
                next_url = None
            return next_url

        next_url = get_one_page_img(detail_url)
        while next_url:
            print(next_url)
            next_url = get_one_page_img(next_url)
        return images_url
