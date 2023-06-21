# coding=utf-8
import execjs

from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = True
    is_serial_number = True
    css_rule = {
        'comic_title': '.works-intro-title strong',
        'chapter_list': '.works-chapter-item',
    }


class ProcessReadPage(BaseProcessReadPage):
    def get_images_url(self, comic_info):
        response = get_response(comic_info['chapter_url'], encoding='utf-8')
        T = re.findall('var DATA.*?\'(.*?)\'', response.text)[0]
        N = re.findall('window\["n.*?e"\]\s=\s(.*?);', response.text)[1]
        js_path = os.path.join(settings.__base_dir__, 'js/_ac_qq.js')
        node_path = os.path.join(settings.__base_dir__, 'js/node_modules')
        ctx = execjs.get().compile(open(js_path, encoding='gb18030').read(), cwd=node_path)
        data = ctx.call('getArr', T, N)

        return {
            'image_links': [picture['url'] for picture in data['picture']],
            'chapter_title': comic_info['chapter_title'],
            'comic_title': comic_info['comic_title']
        }


class SaveLocally(BaseSaveLocally):
    is_make_read = True
