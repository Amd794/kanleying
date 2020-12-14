# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/8/20 15:45
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


# 是否生成h5阅读
MAKE_HTML = True
# 是否生成pdf
MAKE_PDF = True
# 是否进行压缩备份
COMPRESS = False
# rar压缩软件文件路径
EXECUTABLE = r'D:/Sorfwares/WinRAR/WinRAR.exe'

kanleying_type = {
    'detail_lis': '#chapterlistload li',
    'comic_title': '.banner_detail .info h1',
    'comic_pages': 'div.comicpage div',
}
mm820_type = {
    'detail_lis': '.chapter-list li',
    'comic_title': '.title-warper h1',
    'comic_pages': 'div.comiclist div',
}
pc_rules_dict = {

    # https://www.kanleying.com/
    'kanleying': kanleying_type,

    # https://www.hao8.net/
    'hao8': kanleying_type,

    # https://www.kenman123.com/
    'kenman123': kanleying_type,
    
    # http://ikmh88.com/
    'ikmh88': kanleying_type,
    
    # https://www.cswhcs.com/
    'cswhcs': kanleying_type,

    # https://www.kanmanhuala.com/
    'kanmanhuala': kanleying_type,

    # https://www.feixuemh.com/
    'feixuemh': kanleying_type,

    # https://www.hanmanwo.net/
    'hanmanwo': kanleying_type,

    # https://www.bbdmw.com/
    'bbdmw': kanleying_type,

    # https://www.5wmh.com/
    '5wmh': mm820_type,

    # https://www.zuozuomanhua.com/
    'zuozuomanhua': mm820_type,

    # https://www.mm820.com/
    'mm820': mm820_type,

    # https://www.wooowooo.com/
    'wooowooo': mm820_type,

    # https://www.hanmzj.com/
    'hanmzj': mm820_type,

    # https://www.hanmanmi.net/
    'hanmanmi': mm820_type,

    # http://m.haimaoba.com/
    'haimaoba': {
        'detail_lis': '#chapter-list li',
        'comic_title': '.detail-name',
        'comic_pages': '.content img',
    },
    # https://www.hmba.vip/
    'hmba': {
        'detail_lis': '#list dl dd:nth-child(n+4)',
        'comic_title': '.booktitle h1',
        'comic_pages': '#content p:nth-child(2n-1)',
    },
    # https://www.38te.com/
    '38te': {
        'detail_lis': 'ul#detail-list-select li',
        'comic_title': '.info h1',
        'comic_pages': '.comicpage div',
    },
    # https://www.dongmanmanhua.cn/
    'dongmanmanhua': {
        'detail_lis': 'ul#_listUl li',
        'comic_title': '.info h1',
        'comic_pages': '#_imageList > img',
    },
    # https://www.hanmanjie.com/
    'hanmanjie': {
        'detail_lis': '.list div',
        'comic_title': '.container .title',
        'comic_pages': '.read-article figure',
    },
    # https://www.manhuaniu.com/
    'manhuaniu': {
        'detail_lis': 'ul#chapter-list-1 li',
        'comic_title': '.book-title h1 span',
        'comic_pages': '.read-article figure',
    },
    # https://www.nxueli.com/
    'nxueli': {
        'detail_lis': 'ul#chapter-list-1 li',
        'comic_title': '.title h1',
    },
    # https://www.mh1234.com/
    'mh1234': {
        'detail_lis': '#chapter-list-1 li',
        'comic_title': '.title h1',
    },
    # https://www.90ff.com/
    '90ff': {
        'detail_lis': '#chapter-list-1 li',
        'comic_title': '.book-title h1',
    },
    # https://www.36mh.com/
    '36mh': {
        'detail_lis': '#chapter-list-4 li',
        'comic_title': '.book-title h1',
    },
    # https://www.nonomh.com/
    'nonomh': {
        'detail_lis': '.detail-list-select li',
        'comic_title': '.info h1',
        'comic_pages': '#cp_img img',
    },
    # https://www.momomh.com/
    'momomh': {
        'detail_lis': '.detail-list-select li',
        'comic_title': '.detail-main-info-title',
    },
    # https://m.happymh.com/
    'happymh': {
        'comic_title': '.mg-title',
        'comic_pages': '.scan-list div',
    },
    # https://www.love127.com/
    'love127': {
        'detail_lis': '.cy_plist li',
        'comic_title': '.cy_title h1',
    },
    # https://m.733.so/
    '733': {
        'detail_lis': '#list li',
        'comic_title': '.title',
    },
    # http://www.pufei8.com/
    'pufei8': {
        'detail_lis': '.plist li',
        'comic_title': '.titleInfo h1',
    },
    # http://www.taduo.net/
    'taduo': {
        'detail_lis': '.plist li',
        'comic_title': '.titleInfo h1',
    },
    # https://ac.qq.com/
    'qq': {
        'detail_lis': '.works-chapter-item',
        'comic_title': '.works-intro-title strong',
    },
    # https://www.kanman.com/
    'kanman': {
        'detail_lis': '.works-chapter-item',
        'comic_title': '.works-intro-title strong',
    },
    # https://www.cocomanhua.com/
    'cocomanhua': {
        'detail_lis': '.all_data_list li',
        'comic_title': '.fed-deta-content h1',
    },
}

ua = {
    'android': [
          'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36 Edg/87.0.664.41',
          'Mozilla/5.0 (Linux; Android 7.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36 Edg/87.0.664.47',
    ]
}

try:
    from locale_settings import *
except ImportError:
    print('文件不存在')
