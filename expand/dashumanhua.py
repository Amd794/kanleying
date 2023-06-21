import re

import execjs

from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = False
    is_serial_number = True
    css_rule = {
        'comic_title': 'h1.bookname',
        'chapter_list': 'ul#ul_chapter1 li',
    }


class ProcessReadPage(BaseProcessReadPage):
    def get_images_url(self, comic_info):
        eval_code = re.findall(r'else.*(eval.*)}.*var jPicList', get_response(comic_info['chapter_url']).text, re.S)[0]
        js_code = open(os.path.join(settings.__base_dir__, 'js/dashumanhua.js'), encoding='utf-8').read()
        image_links = execjs.get().compile(js_code).call('getImgList', eval_code) # ok 适配完成 测试一下
        return {
            'image_links': image_links,
            'chapter_title': comic_info.get('chapter_title'),
            'comic_title': comic_info.get('comic_title')
        }


class SaveLocally(BaseSaveLocally):
    is_make_read = True


if __name__ == '__main__':
    ProcessReadPage().get_images_url('https://www.dashumanhua.com/comic/qinghuanxu/read-95.html')
