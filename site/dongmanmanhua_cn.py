# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/28 16:31
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import pyquery

from settings import pc_rules_dict
from threading_download_images import get_response


class DongManManHua(object):
    @staticmethod
    def _dongmanmanhua(detail_url, ):
        images_url = []
        detail_url = 'https:' + detail_url
        response = get_response(detail_url)
        pq = pyquery.PyQuery(response.text)
        imgs = pq(pc_rules_dict.get('dongmanmanhua').get('comic_pages'))
        for img in imgs:
            image_url = pyquery.PyQuery(img).attr('data-url')
            images_url.append(image_url)
        return images_url
