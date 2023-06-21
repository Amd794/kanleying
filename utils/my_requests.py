# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2022/4/24 19:56
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


import os
import random
import threading
import warnings
from pprint import pprint

import requests
from fake_useragent import UserAgent
from requests import request
from pathlib import Path

warnings.simplefilter('ignore', RuntimeWarning)
requests.packages.urllib3.disable_warnings()
glock = threading.Lock()
from utils.comic_tools import Util
from typing import Optional
from fake_useragent import settings as fk_ua_settigs

BASE_DIR = Path(__file__).resolve().parent.parent


class MyReq:
    def __init__(self, referer_obj=None, src_link_obj=None):
        """
        :param referer_obj:
        :param src_link_obj:
        """
        fk_ua_settigs.SHORTCUTS.update({
            "huawei": "huawei",
            "apple": "apple",
            "oppo": "oppo",
            "vivo": "vivo",
            "xiaomi": "xiaomi",
            "sanxing": "sanxing",
        })
        self.referer_obj = referer_obj if referer_obj else {}
        self.src_link_obj = src_link_obj if src_link_obj else {}

    def ua(self, is_pc=True):
        """
        todo 返回一个可用的浏览器UserAgent
        :param is_pc: 默认返回pc端ua
        :return: User Agent
        """
        ua = UserAgent(path=os.path.join(BASE_DIR, 'res', 'fake_useragent_0.1.11.json'))
        if is_pc:
            return ua.random
        return random.choice([ua.xiaomi, ua.huawei, ua.apple, ua.oppo, ua.vivo, ua.sanxing])

    def referer(self, src_lnk):
        """
        todo 返回一个header中的referer参数
        :param src_lnk: 请求地址
        :param referer_obj: 字典对象，key为请求地址中存在的某个字符串，value为需要替换为的referer
        :return:
        """
        return self.referer_obj.get(
            next(
                filter(
                    lambda key: key in src_lnk,
                    self.referer_obj
                ),
                'default'
            ),
            src_lnk)

    def handle_lnk(self, src_lnk):
        """
        # todo 处理源链接
        """
        return self.src_link_obj.get(
            next(
                filter(
                    lambda key: key in src_lnk,
                    self.src_link_obj
                ),
                None
            ),
            src_lnk)

    def req_headers(self, src_lnk, header, use_pc_ua=True):
        """
        # todo 构造请求头
        """
        if not header:
            header = {
                'User-Agent': self.ua(use_pc_ua),
                'referer': self.referer(src_lnk),
                # 不缓存
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
            }
        return header

    def send(self,
             url,
             method='GET',
             headers: Optional[dict] = None,
             use_pc_ua: bool = True,
             timeout: int = 25,
             **kwargs
             ):
        if headers is None:
            headers = {}
        res = request(method=method, url=self.handle_lnk(url),
                      headers=self.req_headers(self.handle_lnk(url), headers, use_pc_ua),
                      timeout=timeout,
                      **kwargs)
        return res

    def get_response(self, url, log_output_path='.', max_retries=3, encoding='utf-8', cur_lnk_alias='', **kwargs):
        """
        #   todo 原生requests模块封装了几个自定义参数
        """
        count = 0
        while count < max_retries:
            try:
                response = self.send(url, **kwargs)
                response.raise_for_status()  # 如果status_code不是200,产生异常requests.HTTPError
                response.encoding = encoding
                return response
            except requests.exceptions.RequestException:
                print(
                    f'\033[22;33;22m{url} {0} {cur_lnk_alias}连接超时, 正在进行第{count + 1}次连接重试\033[m'
                )
                count += 1
        print(f'\033[22;31;22m{url}重试{max_retries}次后依然连接失败, 放弃连接...\033[m')
        Util.cre_folder(log_output_path)
        glock.acquire()
        with open(os.path.join(log_output_path, 'error_urls.txt'), 'a') as f:
            f.write(url + ' ' + cur_lnk_alias + '\n')
        glock.release()
        return None


if __name__ == '__main__':
    url = "http://47.98.213.83/api/v1/forward/pinyin"
    response = MyReq(
        referer_obj={
            'pinyi': 6666,
            'pingyi1': eval('9999'),
            'pingyi4': [],
        },
        src_link_obj={
            'http': 'https'
        }
    ).get_response(url, method="post", use_pc_ua=False, data={'text': '牛逼啊', 'heteronym': False, }, timeout=60)
    pprint(response.text)
