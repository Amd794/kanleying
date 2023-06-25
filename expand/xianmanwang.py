import execjs

from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = True
    is_serial_number = True
    css_rule = {
        'comic_title': '.info h1',
        'chapter_list': '#detail-list-select-2 li',
    }


class ProcessReadPage(BaseProcessReadPage):
    def get_images_url(self, comic_info):
        eval_code = re.findall(r'<script>(eval.*?)</script>', get_response(comic_info['chapter_url']).text, re.S)[0]
        js_code = open(os.path.join(settings.__base_dir__, 'js/xianmanwang.js'), encoding='utf-8').read()
        image_links = execjs.get().compile(js_code).call('getImgList', eval_code)
        image_links = ['https://res.xiaoqinre.com/' + path for path in image_links]
        return {
            'image_links': image_links,
            'chapter_title': comic_info.get('chapter_title'),
            'comic_title': comic_info.get('comic_title')
        }


class SaveLocally(BaseSaveLocally):
    is_make_read = True


if __name__ == '__main__':
    ProcessReadPage().get_images_url('https://www.xianmanwang.com/wojialaopolaiziyiqiannianqian/71.html')