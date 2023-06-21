import os
import sys

__base_dir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(__base_dir__, 'expand'))

# 漫画基本信息下载情况保存路径
comic_info_status = os.path.join(__base_dir__, 'res/comic_info_status')
# 漫画保存路径
SAVE_PATH = os.path.join(__base_dir__, 'downloads')
# 是否生成h5阅读
MAKE_HTML = True
# 是否生成pdf
MAKE_PDF = True
# 是否进行压缩备份
COMPRESS = False
# WinRAR程序路径
EXECUTABLE = r'C:/Sorfwares/WinRAR/WinRAR.exe'

# 同一个系统可能部署了n个网站，这些漫画的key会被重制为列表第一个
qinqinmh_website = ['qinqinmh', 'nonomh', 'wzdhm', 'xuxumh', 'jjmhw', 'ikanmh', '91comic', 'mxshm', '592mh', '592hm',
                    '52wxz']

# 配置使用pc UserAgent的网站,默认使用的是手机端ua
use_pc_ua = [
    'qq',
]
# 特效符号处理，替换成全角
special_chars = {
    ',': '，',
    '*': '＊',
    '\\': '＼',
    '\t': ' ',
    '\n': ' ',
    '/': '／',
    '?': '﹖',
    '"': '＂',
    "'": "＇",
    ':': '︰',
    '<': '〈',
    '>': '〉',
    '|': '｜',
    '...': '',
    '…': '',
}

# 纠正章节序号
corrcet_num = {
    # 当前序号-20
    'https://ac.qq.com/Comic/comicInfo/id/647858': 20,
    'https://ac.qq.com/Comic/comicInfo/id/626727': -1,

}
