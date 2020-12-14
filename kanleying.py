# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/3/24 22:37
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


import os
import pathlib
import random
import sys

base_dir = pathlib.Path().absolute()
sys.path.insert(0, os.path.join(base_dir, 'site'))

import pyquery
from PIL import Image, ImageFile
# 简繁转换
from zhconv import convert

ImageFile.LOAD_TRUNCATED_IMAGES = True
from threading_download_images import get_response, download
import settings
import re
import subprocess
import platform as pf

from mm820_com import Mm820
from cswhcs_com import Cswhcs


class Util(object):

    @staticmethod
    def make_pdf(pdf_name, file_list):
        im_list = []

        im1 = Image.open(file_list[0])
        file_list.pop(0)
        for i in file_list:
            img = Image.open(i)
            if img.mode == "RGBA":
                img = img.convert('RGB')
                im_list.append(img)
            else:
                im_list.append(img)
        im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)

    @staticmethod
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
        try:
            with open(save_path, 'w', encoding='utf-8') as w:
                w.write(render_data)
        except FileNotFoundError:
            print('FileNotFoundError: ', save_path)

    @staticmethod
    def compress(target, source, pwd='', delete_source=False, ):
        """
            压缩加密，并删除原数据
            window系统调用rar程序

            linux等其他系统调用内置命令 zip -P123 tar source
            默认不删除原文件
        """
        if pwd: pwd = '-p' + pwd
        if pf.system() == "Windows":
            cmd = f'rar a {pwd} {target} {source} -zcomment.txt'
            p = subprocess.Popen(cmd, executable=settings.EXECUTABLE)
            p.wait()
        else:
            cmd = f'zip a {pwd} {target} {source}'
            p = subprocess.Popen(cmd)
            p.wait()
            # os.system(" ".join(cmd))
        if delete_source:
            os.remove(source)

    @staticmethod
    def exclude_character(s, output='㇑', special_chars=r'''\/:|<･>?*"'''):
        """
            s: str # 需要处理的元数据
            output: str # 替换的字符
            special_chars： str
        """
        for ch in special_chars:
            s = s.replace(ch, output)  # 去除特殊字符并转换为简体中文
        return convert(s, 'zh-hans')


class Comic(Util):
    detail_dicts = []
    current_host_key = ''
    # 是否为章节添加序号
    is_serial_number = ('pufei8', 'qq', 'taduo', 'cocomanhua', 'manhuaniu', '36mh', 'kanman')

    # 获取漫画信息
    @staticmethod
    def get_detail_dicts(url, host_url, host_key) -> list:
        if host_key in ('momomh'):
            url = url.replace('www', 'm', 1)
            print(f'----------{url}-------------')
        response = get_response(url)
        pq = pyquery.PyQuery(response.text)
        Comic.current_host_key = host_key
        rule = settings.pc_rules_dict.get(host_key, '')
        if not rule: raise KeyError(f'{host_url}---->该网站还没有适配')

        if Comic.current_host_key == 'kanman':
            from kanman_com import Kanman
            return Kanman._kanman(url)

        if Comic.current_host_key == 'happymh':
            chapter_list = re.findall('"chapterList":(.*),', response.text)[0]
            chapter_list = eval(chapter_list.replace('false', '0').replace('true', '1'))
            for d in chapter_list:
                detail_dict = {
                    'chapter': Comic.exclude_character(d['chapterName']),
                    'chapter_url': url + '/' + d['id'],
                    'comic_title': pq('.mg-title').text(),
                }
                Comic.detail_dicts.append(detail_dict)
            return Comic.detail_dicts[::-1]

        def detail_one_page(detail_url):
            response = get_response(detail_url)
            if Comic.current_host_key in ('momomh',):
                response = get_response(detail_url, header={'User-Agent': random.choice(settings.ua['android'])})
            if Comic.current_host_key in ('haimaoba', 'pufei8', 'taduo'):
                response = get_response(detail_url, encoding='gbk')
            pq = pyquery.PyQuery(response.text)
            lis = pq(rule.get('detail_lis'))
            comic_title = pq(rule.get('comic_title')).text()
            if '最终话' in Comic.exclude_character(comic_title):
                comic_title = Comic.exclude_character(comic_title + '（完结）')
            if Comic.current_host_key == '18comic':
                comic_title = comic_title[(len(comic_title) // 2) + 1:]
            if Comic.current_host_key == '18comic':
                if not lis.length:
                    detail_dict = {
                        'chapter': '共一话',
                        'chapter_url': host_url + pq('div.read-block a:first-child').attr('href').lstrip('/'),
                        'comic_title': Comic.exclude_character(comic_title) + '（完结）',
                    }
                    Comic.detail_dicts.append(detail_dict)
                    return Comic.detail_dicts
            for li in lis:
                chapter = pyquery.PyQuery(li)('a').text()
                # 重构章节名称 001+标题
                if Comic.current_host_key in Comic.is_serial_number:
                    if host_key in ('qq', 'manhuaniu', '36mh', 'kanman'):
                        chapter = str(lis.index(li) + 1).rjust(3, '0') + " " + chapter
                    else:
                        chapter = str(lis[::-1].index(li) + 1).rjust(3, '0') + " " + chapter
                chapter_url = pyquery.PyQuery(li)('a').attr('href')
                if Comic.current_host_key == 'dongmanmanhua':
                    chapter = chapter.split('･')[0]
                detail_dict = {
                    'chapter': Comic.exclude_character(chapter),
                    'chapter_url': host_url + chapter_url.lstrip('/') if host_key not in chapter_url else chapter_url,
                    'comic_title': Comic.exclude_character(comic_title),
                }
                Comic.detail_dicts.append(detail_dict)

        detail_one_page(url)
        # 处理特殊情况 pyquery 好像不支持nth-child(n+3)这种类型过滤
        if Comic.current_host_key == 'hmba':
            Comic.detail_dicts = Comic.detail_dicts[9:]
        if Comic.current_host_key == 'dongmanmanhua':
            total_pages = len(pq('.paginate a'))
            for i in range(2, total_pages + 1):
                detail_one_page(url + f'&page={i}')
            Comic.detail_dicts.reverse()
        if Comic.current_host_key == '18comic':
            try:
                if len(Comic.detail_dicts[0]['chapter']) > len(Comic.detail_dicts[1]['chapter']):
                    Comic.detail_dicts[0]['chapter'] = Comic.detail_dicts[0]['chapter'].replace(
                        Comic.detail_dicts[0]['comic_title'], '1 ')
                    Comic.detail_dicts[-1]['chapter'] = Comic.detail_dicts[-1]['chapter'].replace('最新', '')
            except IndexError:
                print('短篇漫画')
            return Comic.detail_dicts
        if Comic.current_host_key in ('733', 'pufei8', 'taduo', 'cocomanhua'):
            return Comic.detail_dicts[::-1]
        return Comic.detail_dicts

    # 获取漫画图片
    @staticmethod
    def get_images_url(detail_dict: dict) -> dict:
        if Comic.current_host_key == 'kanman':
            return detail_dict
        cswhcs_type = ('cswhcs', 'kanleying', 'qinqinmh')
        mm820_type = ('mm820', 'hanmzj')

        detail_url = detail_dict.get('chapter_url')
        chapter = detail_dict.get('chapter')
        comic_title = detail_dict.get('comic_title')

        feifan_mod_type = 'from feifan import Feifan'
        feifan_data_type = 'Feifan._nxueli(detail_url, Comic.current_host_key)'
        m_733_mod_type = 'from m_733_so import M733So'
        m_733_data_type = 'M733So._733(detail_url)'
        taduo_mod_type = 'from pufei8_com import PuFei8'
        taduo_data_type = 'PuFei8.get_images_url(detail_url)'

        mod = {
            '733': m_733_mod_type,
            'love127': m_733_mod_type,
            'pufei8': taduo_mod_type,
            'taduo': taduo_mod_type,
            'qq': 'from ac_qq_com import AcQq',
            'momomh': 'from momomh_com import Momomh',
            'happymh': 'from m_happymh_com import Happymh',
            'cocomanhua': 'from cocomanhua_com import CoCoManHua',
            'dongmanmanhua': 'from dongmanmanhua_cn import DongManManHua',
            'haimaoba': 'from m_haimaoba_com import HaiMaoBa',
            'nxueli': feifan_mod_type,
            '90ff': feifan_mod_type,
            'manhuaniu': feifan_mod_type,
            '36mh': feifan_mod_type,
            'mh1234': feifan_mod_type,
        }
        data = {
            '733': m_733_data_type,
            'love127': m_733_data_type,
            'pufei8': taduo_data_type,
            'taduo': taduo_data_type,
            'qq': 'AcQq._ac_qq(detail_url)',
            'happymh': 'Happymh._happymh(detail_url)',
            'momomh': 'Momomh._momomh(detail_url)',
            'cocomanhua': 'CoCoManHua._cocomanhua(detail_url)',
            'dongmanmanhua': 'DongManManHua._dongmanmanhua(detail_url)',
            'haimaoba': 'HaiMaoBa._haimaoba(detail_url)',
            'nxueli': feifan_data_type,
            '90ff': feifan_data_type,
            'manhuaniu': feifan_data_type,
            '36mh': feifan_data_type,
            'mh1234': feifan_data_type,
        }

        exec(mod.get(Comic.current_host_key, ''))
        images_url = eval(data.get(Comic.current_host_key, '[]'))
        if images_url:
            return {'images_url': images_url, 'chapter': chapter, 'comic_title': comic_title}

        def parse_images_url(url):
            if Comic.current_host_key in ('nonomh', 'qinqinmh', 'wzdhm'):
                header = {
                    'User-Agent': random.choice(settings.ua['android']),
                }
                response = get_response(url, header=header)
            else:
                response = get_response(url)
            pq = pyquery.PyQuery(response.text)
            divs = pq(settings.pc_rules_dict.get(Comic.current_host_key).get('comic_pages'))
            for div in divs:
                if Comic.current_host_key in ('nonomh', 'qinqinmh', 'wzdhm'):
                    img_src = pyquery.PyQuery(div).attr('data-original')
                else:
                    img_src = pyquery.PyQuery(div)('img').attr('data-original')
                    if not img_src:
                        img_src = pyquery.PyQuery(div)('img').attr('src')
                images_url.append(img_src)
            return pq

        pq = parse_images_url(detail_url)
        #  处理特殊情况
        if Comic.current_host_key in cswhcs_type:
            images_url.extend(Cswhcs._cswhcs(pq))
        if Comic.current_host_key in mm820_type:
            # 获取分页数
            pages = len(pq('.selectpage option'))
            images_url.extend(Mm820._mm820(detail_url, pages))
        if Comic.current_host_key == '18comic':
            images_url = [img for img in images_url if img]  # 排除空元素
            images_url = [img for img in images_url if not img.startswith('/static/')]
            if len(images_url) > 499:
                n = pq('#pageselect > option:nth-child(1)').text().split('/')[1]
                for i in range(501, int(n) + 1):
                    images_url.append(re.sub('\d+\.jpg', f'{i}.jpg'.rjust(9, '0'), images_url[0]))
        if Comic.current_host_key == 'ikmh88':
            images_url = [image_url.replace('\n', '') for image_url in images_url]

        return {'images_url': images_url, 'chapter': chapter, 'comic_title': comic_title}

    # 下载漫画
    @staticmethod
    def download_images(images_dict, chapters):
        images_url = images_dict.get('images_url')
        chapter = images_dict.get('chapter').strip(' ')
        comic_title = images_dict.get('comic_title').strip(' ')
        print(f'开始下载{comic_title}-{chapter}\n')
        file_path = f'./{os.path.basename(__file__).strip(".py")}/{comic_title}/{chapter}/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if 'mhpic' in images_url[0]:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
                'Referer': 'http://www.manhuatai.com/cjtksdcz/xz.html?from=kmhapp',
            }
            download(images_url, file_path, 6, headers, )
        download(images_url, file_path, 6)

        def f(sl):
            try:
                return int(re.findall('(\d+)\.jpg', sl)[0])
            except IndexError:
                return 999

        suffix = ['jpg', 'png', 'gif', 'jpeg']
        file_list = sorted(
            [file_path + str(imgFileName) for imgFileName in os.listdir(file_path) if
             imgFileName.endswith(tuple(suffix))],
            key=f
        )
        if not len(f'{comic_title}-{chapter}') > 58:
            file_name = f'{file_path}/{comic_title}-{chapter}'.replace('//', '/')
        else:
            file_name = f'{file_path}/{chapter}'.replace('//', '/')

        if settings.MAKE_HTML:
            print(f'开始生成html{comic_title}-{chapter}\n')
            Comic.render_to_html(f'{file_name}.html', chapter, comic_title,
                                 [str(x) + '.jpg' for x in range(len(file_list))], chapters)
        if settings.MAKE_PDF:
            print(f'开始生成PDF{comic_title}-{chapter}\n')
            Comic.make_pdf(f'{file_name}.pdf', file_list)
        if settings.COMPRESS:
            comment = {
                'Website': 'https://amd794.com',
                'Password_1': '百度云',
                'Password_2': f'{comic_title}-{chapter}',
            }
            with open(f'{file_path}/Password.txt', 'w', encoding='utf-8') as f:
                f.write(str(comment))
            print(f'开始压缩文件{comic_title}-{chapter}\n')
            Comic.compress(f'{file_name}.rar', f'{file_path}/*', f'{comic_title}-{chapter}')


def main():
    while True:
        url = input('漫画地址:').strip()
        if url == 'q':
            break
        try:
            host_key = re.match('https?://\w+\.(.*?)\.\w+/', url).group(1)  # kanleying
            host_url = re.match('https?://\w+\.(.*?)\.\w+/', url).group()  # https://www.kanleying.com/
        except AttributeError:
            host_key = re.match('https?://(.*?)\.\w+/', url).group(1)  # kanleying
            host_url = re.match('https?://(.*?)\.\w+/', url).group()  # https://kanleying.com/

        print(host_url, host_key)
        detail_dicts = Comic.get_detail_dicts(url, host_url, host_key)
        chapters = [detail_dict['chapter'] for detail_dict in detail_dicts]
        print(f'该漫画共{len(chapters)}章节')

        def run(detail_dict):
            # print(detail_dict)
            images_dict = Comic.get_images_url(detail_dict)
            Comic.download_images(images_dict, chapters)

        while True:
            ipt = input('>>>:')
            if ipt == 'q':
                # 清空一下残留数据
                Comic.detail_dicts = []
                break
            char = re.findall('\D+', ipt)
            index = re.findall('\d+', ipt)
            print(f'char:{char}  index:{index}')
            chars = {
                '+': 'detail_dicts[int(index[0]):]',
                '/': 'detail_dicts[int(index[0]): int(index[1])]',
                '-': 'detail_dicts[int(index[0])-2::-1],',
                '*': str([detail_dicts[i - 1] for i in list(map(int, index))]),
            }

            if char:
                d = chars.get(char[0], '不存在')
                print(d)
                for detail_dict in eval(d):
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


if __name__ == '__main__':
    main()
