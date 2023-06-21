import json
import os
import re
import sys

__base_dir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, __base_dir__)
from importlib import import_module

from conf import settings


class Comic:
    def __init__(self, url):
        self.host_url = None
        self.host_key = None
        self.chapters = None
        self.comic_info = None
        self.module_obj = None
        self.url = url

    def handle_host_key(self, ):
        """
        todo 给同类型网站重写host key
        """
        same_site = [
            settings.qinqinmh_website,
            settings.mh1234_website,
        ]
        self.host_key = next(
            filter(
                lambda keys: self.host_key in keys, same_site),
            [self.host_key]
        )[0]

    def run(self, detail_dict):
        image_links = getattr(self.module_obj, 'ProcessReadPage')().get_images_url(detail_dict)
        getattr(self.module_obj, 'SaveLocally')().save(image_links, self.chapters)

    def load_mh_info(self):
        self.host_url, self.host_key = re.findall(r'(https?://(?:\w+\.)?(.*?)\.\w+/)', self.url)[0]
        self.handle_host_key()
        print(f'{self.host_key}, {self.host_url}')
        self.module_obj = import_module(f'{self.host_key}')
        comic_info = getattr(self.module_obj, f'ProcessDetailsPage')(self.url, self.host_url, self.host_key).comic_info
        self.comic_info, self.chapters = comic_info, [item['chapter_title'] for item in comic_info]
        print(f'该漫画共{len(self.chapters)}章节')
        with open(f'chapters_info.json', 'w', encoding='utf-8') as fw:
            fw.write(json.dumps(self.chapters, ensure_ascii=False, indent=4, separators=(', ', ': ')))

    def btch_download(self):
        try:
            # ['http://m.jdkbcomic.com/24001/', ] 批量下载最新一章节
            if isinstance(eval(self.url), list):
                for self.url in eval(self.url):
                    self.load_mh_info()
                    for detail_dict in self.comic_info[-2:]:
                        self.run(detail_dict)
                return True
            # ('https://miccomic.art/album/274556/', ) 批量下载全部章节
            if isinstance(eval(self.url), tuple):
                for self.url in eval(self.url):
                    # 在追加新的漫画进去前读取信息
                    with open('../res/comic_info_status', encoding='utf-8') as fr:
                        comic_info = fr.readlines()
                    self.load_mh_info()
                    tuple_dl_comic_title = self.comic_info[0]["comic_title"]
                    if tuple_dl_comic_title + '\n' in comic_info:
                        print(f'{tuple_dl_comic_title} 已经下载过')
                        continue
                    # 备注一些不是短篇漫画
                    if len(self.chapters) > 1 and self.host_key in settings.comic18_website:
                        with open(f'{settings.SAVE_PATH}/待确认的漫画.txt', 'a',
                                  encoding='utf-8') as fa:
                            fa.write(f'"{tuple_dl_comic_title}": "{self.url}",\n')
                    for detail_dict in self.comic_info:
                        self.load_mh_info()
                        self.run(detail_dict)
                return True
        except SyntaxError:
            pass

    def download_by_cmd(self, ipt):
        char = re.findall(rf'[+/*]', ipt)
        index = re.findall(r'-?\d+', ipt)
        difference = settings.corrcet_num.get(self.url, 0)
        print(f'char:{char}  index:{index}  difference:{difference}')
        chars = {
            '+': 'self.comic_info[int(index[0]) + difference:]',
            '/': 'self.comic_info[int(index[0]) + difference + 1: int(index[1]) + difference]',
            '*': str(list(map(lambda i: self.comic_info[i + difference - 1], map(int, index)))),
        }

        if char:
            d = chars.get(char[0], '不存在')
            for detail_dict in eval(d):
                self.run(detail_dict)
        else:
            if index:
                if index == ['0']:
                    for detail_dict in self.comic_info:
                        self.run(detail_dict)
                else:
                    if '-' in index[0]:
                        self.run(self.comic_info[int(index[0]) - 1])
                    else:
                        self.run(self.comic_info[int(index[0]) - 1 + settings.corrcet_num.get(self.url, 0)])
            else:
                self.run(self.comic_info.pop())

    def main(self):
        while True:
            if self.url == 'q':
                break
            if self.btch_download():
                return
            self.load_mh_info()
            while True:
                ipt = input('>>>:')
                if ipt == 'q':
                    self.comic_info = []
                    self.url = input('地址:').strip().encode("utf-8").decode("latin1")
                    break
                self.download_by_cmd(ipt)


if __name__ == '__main__':
    obj = Comic(input('地址:').strip().encode("utf-8").decode("latin1"))
    obj.main()
