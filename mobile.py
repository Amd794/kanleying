# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/9/8 11:49
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

import re

import requests
from pyquery import PyQuery
# 简繁转换
from zhconv import convert

from kanleying import Comic


def detail_chapter(test_url, host_url):
    detail_dicts = []
    header = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/85.0.4183.83',
        'referer': test_url,
    }
    text = requests.get(test_url, headers=header).text
    comic_title = PyQuery(text)('.detail-main-info-title').text()
    for ch in r'\/:|<.･>?*"':
        comic_title = comic_title.replace(ch, '㇑')  # 去除特殊字符
    for li_tag in PyQuery(text)('.detail-list-select li'):
        chapter = PyQuery(li_tag)('a').text()
        for ch in r'\/:|<.･>?*"':
            chapter = chapter.replace(ch, '㇑')  # 去除特殊字符
        a_href = PyQuery(li_tag)('a').attr('href')
        detail_dict = {
            'chapter': convert(chapter, 'zh-hans'),
            'a_href': host_url + a_href,
            'comic_title': convert(comic_title, 'zh-hans'),
        }
        detail_dicts.append(detail_dict)
    return detail_dicts


def get_chapter_images(detail_dict, chapters):
    url = detail_dict.get('a_href')
    imgs = []
    header = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/85.0.4183.83',
        'referer': url,
    }
    text = requests.get(url, headers=header).text
    for img_tag in PyQuery(text)('#cp_img img'):
        imgs.append(PyQuery(img_tag).attr('data-original'))

    Comic.download_images(
        {
            'images_url': imgs,
            'chapter': detail_dict['chapter'],
            'comic_title': detail_dict['comic_title'],
        },
        chapters
    )


if __name__ == '__main__':
    while True:
        url = input('漫画地址（手机）:').strip()
        try:
            host_key = re.match('https?://\w+\.(.*?)\.\w+/', url).group(1)  # kanleying
            host_url = re.match('https?://\w+\.(.*?)\.\w+/', url).group()  # https://www.kanleying.com/
        except AttributeError:
            host_key = re.match('https?://(.*?)\.\w+/', url).group(1)  # kanleying
            host_url = re.match('https?://(.*?)\.\w+/', url).group()  # https://kanleying.com/
        detail_dicts = detail_chapter(url, host_url)
        Comic.detail_dicts = detail_dicts
        chapters = [detail_dict['chapter'] for detail_dict in detail_dicts]


        def run(detail_dict):
            get_chapter_images(detail_dict, chapters)


        while True:
            ipt = input('>>>:')
            if ipt == 'q':
                break
            char = re.findall('\D+', ipt)
            index = re.findall('\d+', ipt)
            print(f'char:{char}  index:{index}')
            try:
                chars = {
                    '+': detail_dicts[int(index[0]):],
                    '-': detail_dicts[int(index[0]) - 2::-1],
                    '*': [detail_dicts[i - 1] for i in list(map(int, index))],
                }
            except IndexError:
                chars = {}

            # 下载某章节之后所有章节
            if char:
                for detail_dict in chars.get(char[0], '不存在'):
                    run(detail_dict)
            else:
                if index:
                    if index == ['0']:
                        for detail_dict in detail_dicts:
                            run(detail_dict)
                    else:
                        run(detail_dicts[int(index[0]) - 1])
                else:
                    run(detail_dicts.pop())
