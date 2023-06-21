# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2021/12/7 11:05
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794
import os
import pathlib
import platform as pf
import re
import subprocess
import typing as t

from PIL import Image, UnidentifiedImageError
from jinja2 import Environment, FileSystemLoader
# 简繁转换
from zhconv import convert

from conf import settings as settings


# from stub import typ


class Util(object):
    @staticmethod
    def make_pdf(
            pdf_name: str,
            file_list: list[str, str]
    ) -> None:
        """
        todo 生成pdf阅读文件
        :param pdf_name: 文件名称
        :param file_list: 一个只包含图片的列表
        :return: None
        """
        im_list = []
        try:
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
        except (UnidentifiedImageError, ValueError):
            pass

    @staticmethod
    def render_to_html(
            save_path,
            cur_chap: str,
            comic_title: str,
            pic_lst: t.Sequence[str],
            chap_titls: t.Sequence[str],
            tmpl_root_dir='../templates'
    ) -> None:
        """
        todo 生成html阅读文件
        :param save_path: 生成的阅读文件后的保存路径
        :param cur_chap: 当前阅读的章节名称
        :param comic_title: 漫画名称
        :param pic_lst: 一个只包含图片链接的列表
        :param chap_titls: 一个只包含章节名称的列表
        :param tmpl_root_dir: 存放模板文件的根目录
        :return: None
        """
        env = Environment(loader=FileSystemLoader(tmpl_root_dir))
        template = env.get_template('reader.html')
        result = template.render(comic_title=comic_title,
                                 cur_chap=cur_chap,
                                 chap_titls=enumerate(chap_titls),
                                 pic_lst=pic_lst,
                                 chapter_num=len(chap_titls))

        try:
            with open(save_path, 'w', encoding='utf-8') as w:
                w.write(result)
        except FileNotFoundError:
            print('FileNotFoundError: ', save_path)

    @staticmethod
    def compress(target, source, pwd='', delete_source=False, ):
        """
        todo
            压缩加密，并删除原数据
            window系统调用rar程序
            linux等其他系统调用内置命令 zip -P123 tar source
            默认不删除原文件是
        :param target: 输出文件路径
        :param source: 输入的文件路径
        :param pwd: 设置加密的密码， 默认为空
        :param delete_source: 压缩后是否删除源文件，默认不删除
        :return:
        """
        if pwd: pwd = '-p' + pwd
        if pf.system() == "Windows":
            # 加上双引号防止文件路径存在空格造成命令错误
            cmd = f'rar a "{pwd}" "{target}" "{source}" -zcomment.txt'
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
    def exclude_character(
            a_str: str
    ) -> str:
        """
        todo 处理字符串
        :param a_str: 原始的字符串
        :return: 处理后的字符串
        """
        for ch in settings.special_chars:
            a_str = a_str.replace(ch, settings.special_chars[ch])  # 去除特殊字符并转换为简体中文
            a_str = re.sub(' {2，9}', '　', a_str)  # 去除多余空格
        if len(a_str) > 100:
            a_str = a_str[:100]
        return convert(a_str.strip(), 'zh-hans')

    @staticmethod
    def cre_folder(
            folder_path
    ) -> None:
        """
        todo 创建文件夹
        :param folder_path: 文件路径
        :return: None
        """
        folder_path = os.path.dirname(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'创建文件夹：{folder_path}')


if __name__ == '__main__':
    Util.render_to_html('test.html', '15', 'comic_title', [f'{_}.jpg' for _ in range(20)],
                        [str(_) for _ in range(20)], )
