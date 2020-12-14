# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/11/6 15:21
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os
import pathlib
import re


def render_to_html(save_path, chapter, comic_title, imgs: list, chapters, template_path='template.html', ):
    """
        save_path: 生成的html保存路径
        chapter: 当前章节名称
        comic_title: 漫画名称
        imgs : 图片路径
        chapters: list 所有章节名称
        template_path: 渲染模板路径
    """
    chapter_num = len(chapters)
    imgs_html = ''
    lis_html = ''
    for img in imgs:
        imgs_html += f'<img src="{img}" alt="" style="width: 100%">\n'
    for li in range(chapter_num):
        lis_html += f'''<li id="current_{li + 1}"><a href="../{chapters[li]}/{comic_title}-{chapters[li]}.html#active" rel="nofollow" title="{chapters[li]}">{chapters[li]}</a></li>\n'''
    with open(template_path, 'r', encoding='utf-8') as r:
        render_data = re.sub('{{title}}', chapter, r.read())
        render_data = re.sub('{{imgs}}', imgs_html, render_data)
        render_data = re.sub('{{lis_html}}', lis_html, render_data)
        render_data = re.sub('{{chapter_num}}', str(chapter_num), render_data)

    with open(save_path, 'w', encoding='utf-8') as w:
        w.write(render_data)


def repr_html():
    def f(l):
        try:
            return int(re.findall('\d+', l)[0])
        except IndexError:
            return 999

    base_dir, comic_title = os.path.split(pathlib.Path().absolute())
    chapters = os.listdir('.')
    chapters.remove(os.path.basename(__file__))
    chapters.sort(key=f)
    print(f'basedir: {base_dir}')
    print(f'chapters: {chapters}')
    input('-------—确认章节排序没问题后就按回车继续执行—------')
    print(f'comic_title: {comic_title}')
    for chapter in chapters:
        print(f'chapter: {chapter}')
        file_name = f'{base_dir}/{comic_title}/{chapter}/{comic_title}-{chapter}.html'
        print(f'file_path: {file_name}')
        suffix = ['jpg', 'png', 'gif', 'jpeg']
        file_list = [str(imgFileName) for imgFileName in os.listdir(f'./{chapter}') if
                     imgFileName.endswith(tuple(suffix))]
        file_list.sort(key=f)
        print(f'file_list: {file_list}')
        render_to_html(file_name, chapter, comic_title, file_list, chapters,
                       template_path=r'C:\Users\29522\Desktop\Project\PyCharm\Python_fullstack\5. 网络爬虫\韩漫\template.html')
    print('全部完成')
    os.remove(__file__)


if __name__ == '__main__':
    repr_html()
