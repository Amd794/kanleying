# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/10/31 15:47
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import re

from threading_download_images import get_response


class Feifan(object):
    @staticmethod
    def _nxueli(detail_url, current_host_key):
        response = get_response(detail_url)
        chapter_path_regix = 'chapterPath = "(.*?)"'
        chapter_images = eval(re.sub(r'\\', '', re.search('chapterImages = (\[.*?\])', response.text).group(1)))
        if current_host_key == 'nxueli':
            return ['https://images.nxueli.com' + i for i in chapter_images]
        elif current_host_key == '90ff':
            chapter_path = re.search(chapter_path_regix, response.text).group(1)
            return [f'http://90ff.bfdblg.com/{chapter_path}' + i for i in chapter_images]
        elif current_host_key == 'mh1234':
            chapter_path = re.search(chapter_path_regix, response.text).group(1)
            return [f'https://img.wszwhg.net/{chapter_path}' + i for i in chapter_images]
        elif current_host_key == '36mh':
            chapter_path = re.search(chapter_path_regix, response.text).group(1)
            return [f'https://img001.shmkks.com/{chapter_path}' + i for i in chapter_images]
        elif current_host_key == 'manhuaniu':
            return ['https://restp.dongqiniqin.com/' + i for i in chapter_images]