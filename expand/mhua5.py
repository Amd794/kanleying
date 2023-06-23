from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = True  # 章节倒序
    css_rule = {
        'comic_title': '.de-info__box p.comic-title',
        'chapter_list': 'div.chapter__list li',
    }


class ProcessReadPage(BaseProcessReadPage):
    img_ele_attr = 'data-original'
    css_rule = {
        'image_link': '.rd-article__pic img',
    }


class SaveLocally(BaseSaveLocally):
    is_make_read = True  # 生成阅读文件
