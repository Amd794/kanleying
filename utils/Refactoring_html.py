# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/11/6 15:21
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os
import pathlib
import re

from comic_tools import Util


def repr_html():
    def f(l):
        try:
            if 'Preview' in l:
                return -1
            return int(re.findall('\d+', l)[0])
        except IndexError:
            return 999

    base_dir, comic_title = os.path.split(pathlib.Path().absolute())
    chapters = [comic for comic in os.listdir('.') if os.path.isdir(comic) and not comic.startswith('.')]
    chapters.sort(key=f)
    print(f'basedir: {base_dir}')
    print(f'chapters: {chapters}')
    input('-------—确认章节排序没问题后就按回车继续执行—------')
    print(f'comic_title: {comic_title}')
    for chapter in chapters:
        html_file = sorted(
            [str(imgFileName) for imgFileName in os.listdir(chapter) if
             imgFileName.endswith(tuple('.html'))],
            key=f
        )
        # 清理旧模板文件
        [os.remove(f'{base_dir}/{comic_title}/{chapter}/{file}') for file in html_file]
        print(f'chapter: {chapter}')
        file_name = f'{base_dir}/{comic_title}/{chapter}/{comic_title}-{chapter}.html'
        print(f'file_path: {file_name}')
        suffix = ['jpg', 'png', 'gif', 'jpeg']
        file_list = [str(imgFileName) for imgFileName in os.listdir(f'./{chapter}') if
                     imgFileName.endswith(tuple(suffix))]
        file_list.sort(key=f)
        print(f'file_list: {file_list}')
        Util.render_to_html(file_name, chapter, comic_title, file_list, chapters,
                            r'C:\Users\29522\Desktop\Project\5. 网络爬虫\comic_downloader\templates\reader.html')
    print('全部完成')
    os.remove(__file__)


if __name__ == '__main__':
    repr_html()
