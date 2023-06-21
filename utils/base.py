import json
import os
import re
from functools import lru_cache

from pyquery import PyQuery

from utils.comic_tools import Util
from conf import settings
from utils.downloader import get_response, async_down


class BaseProcessDetailsPage:
    """
    todo 处理详情页
    """

    # 默认配置
    encoding = 'utf-8'
    is_serial_number = False
    is_reversal_chapter = False
    css_rule = {
        'comic_title': '',
        'chapter_list': '',
    }

    def __init__(self, input_url, host_url, host_key):
        # 传入参数+
        self.input_url = input_url
        self.host_url = host_url
        self.host_key = host_key
        self.comic_title = ''
        self.chapter_title = ''
        self.html = None


    @property
    def read_comic_title_list(self):
        if not os.access(settings.comic_info_status, os.F_OK):
            print(f'-----{settings.comic_info_status}不存在------')
            with open(settings.comic_info_status, 'w', encoding='utf-8') as fw:
                fw.write('')
        with open(settings.comic_info_status, encoding='utf-8') as fr:  # 读取本地漫画状态
            comic_title_list = fr.readlines()
        return comic_title_list

    def rewrite_comic_title(self, old_title, *args, **kwargs):
        """
        todo 重写漫画标题
        """
        return old_title

    def rewrite_chapter_title(self, old_title, *args, **kwargs):
        """
        todo 重写漫画章节标题
        """
        return old_title

    def add_serl_numbers_to_chapters(self, chapter_title, chapter_ele_list, chapter_ele):
        """
        todo 给章节添加序号
        """
        diff_num = settings.corrcet_num.get(self.input_url, 0)

        return str(chapter_ele_list.index(chapter_ele) - diff_num).rjust(4, '0') + " " + chapter_title

    def save_comic_info(self, *args, **kwargs):
        """
        todo 保存漫画基本信息
        """
        pass

    @property
    @lru_cache
    def comic_info(self) -> list:
        """
        todo 解析页面获取漫画详情数据.
        """
        comic_info = []
        response = get_response(self.input_url, encoding=self.encoding)
        self.html = PyQuery(response.text)
        self.comic_title = self.rewrite_comic_title(self.html(self.css_rule.get('comic_title')).text())
        if self.css_rule['chapter_list'] == 'pass':
            chapter_ele_list = [f'<a href="{self.input_url}"></a>']
        else:
            chapter_ele_list = self.html(self.css_rule['chapter_list'])
        self.save_comic_info()
        if not self.is_reversal_chapter:
            chapter_ele_list.reverse()
        for chapter_ele in chapter_ele_list:
            self.chapter_title = self.rewrite_chapter_title(PyQuery(chapter_ele)('a').text())
            chapter_url = PyQuery(chapter_ele)('a').attr('href')
            if self.is_serial_number:
                self.chapter_title = self.add_serl_numbers_to_chapters(self.chapter_title, chapter_ele_list, chapter_ele)
            comic_info.append({
                'chapter_title': Util.exclude_character(self.chapter_title),
                'chapter_url': self.host_url + chapter_url.lstrip('/') if all(['http' not in chapter_url, chapter_url]) else chapter_url,
                'comic_title': Util.exclude_character(self.comic_title),
            })
        return comic_info


class BaseProcessReadPage:
    """
    todo 处理阅读页
    """

    css_rule = {
        'image_link': ''
    }
    img_ele_attr = ''

    def __init__(self):
        self.comic_title = None
        self.chapter_title = None
        self.chapter_url = None

    def img_src(self, ele):
        """
        todo 定义不同的提取规则提取img标签src中的图片链接
        """
        img_src = PyQuery(ele)('img').attr('src')
        if self.img_ele_attr:
            img_src = PyQuery(ele).attr(self.img_ele_attr)

        return img_src

    def process_image_links(self, image_links):
        return image_links

    def image_links(self, chapter_url):
        image_links = []
        response = get_response(chapter_url)
        html = PyQuery(response.text)
        images_ele = html(self.css_rule.get('image_link'))
        for image_ele in images_ele:
            image_links.append(self.img_src(image_ele))
        return self.process_image_links(image_links)

    def process_other_operate(self):
        pass

    def get_images_url(self, comic_info):
        """
        todo 获取单个章节的图片链接。
        """
        self.chapter_url = comic_info.get('chapter_url')
        self.chapter_title = comic_info.get('chapter_title')
        self.comic_title = comic_info.get('comic_title')
        self.process_other_operate()
        return {
            'image_links': self.image_links(self.chapter_url),
            'chapter_title': self.chapter_title,
            'comic_title': self.comic_title
        }


class BaseSaveLocally:
    """
    todo 下载
    """

    is_make_read = False

    def __init__(self):
        self.file_path = None
        self.comic_title = None
        self.chapter_title = None
        self.image_links = None

    @staticmethod
    def srt_by_numbers(sl):
        try:
            return list(map(int, re.findall('(\d+)', sl)))
        except IndexError:
            if '最终' in sl:
                return 888
            elif '后记' in sl:
                return 999
            elif '序章' in sl:
                return -1
            elif 'Preview' in sl:
                return -2
            return 999

    def serialized_file(self, ):
        suffix = ['jpg', 'png', 'gif', 'jpeg']
        file_list = sorted(
            [self.file_path + str(imgFileName) for imgFileName in os.listdir(self.file_path) if
             imgFileName.endswith(tuple(suffix))],
            key=self.srt_by_numbers
        )
        if len(f'{self.comic_title}-{self.chapter_title}') < 58:
            file_name = f'{self.file_path}/{self.comic_title}-{self.chapter_title}'.replace('//', '/')
        else:
            file_name = f'{self.file_path}/{self.chapter_title}'.replace('//', '/')
        return file_list, file_name

    def process_image_file(self, file_list, *args, **kwargs):
        """
        todo 处理comic18网站的图片混淆
        """
        pass

    def extra_build(self, file_name, file_list, chapters):
        if settings.MAKE_HTML:
            print(f'开始生成html{self.comic_title}-{self.chapter_title}\n')
            Util.render_to_html(f'{file_name}.html', self.chapter_title, self.comic_title,
                                [str(x) + '.jpg' for x in range(len(file_list))], chapters)
        if settings.MAKE_PDF:
            print(f'开始生成PDF{self.comic_title}-{self.chapter_title}\n')
            Util.make_pdf(f'{file_name}.pdf', file_list)
        if settings.COMPRESS:
            comment = {
                'Website': 'https://amd794.com',
                'Password_1': '百度云',
                'Password_2': f'{self.comic_title}-{self.chapter_title}',
            }
            with open(f'{self.file_path}/Password.txt', 'w', encoding='utf-8') as f:
                f.write(json.dumps(comment, ensure_ascii=False, indent=2, separators=(',', ': ')))
            print(f'开始压缩文件{self.comic_title}-{self.chapter_title}\n')
            Util.compress(f'{file_name}.rar', f'{self.file_path}/*', f'{self.comic_title}-{self.chapter_title}')

    def save(self, images_dict, chapters) -> None:
        """
        todo 下载漫画章节图片.
        """
        self.image_links = images_dict.get('image_links')
        self.chapter_title = images_dict.get('chapter_title')
        self.comic_title = images_dict.get('comic_title')
        self.file_path = f'{settings.SAVE_PATH}/{self.comic_title}/{self.chapter_title}/'
        print(f'开始下载{self.comic_title}-{self.chapter_title}\n')
        Util.cre_folder(self.file_path)
        async_down(self.image_links, self.file_path)
        if not self.is_make_read:
            print('不执行压缩、合成PDF、生成h5阅读'.center(100, '-'))
            return

        file_list, file_name = self.serialized_file()
        self.process_image_file(file_list)
        self.extra_build(file_name, file_list, chapters)
