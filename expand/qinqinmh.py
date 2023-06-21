from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = True
    css_rule = {
        'comic_title': 'p.detail-main-info-title',
        'chapter_list': '#detail-list-select li',
    }


class ProcessReadPage(BaseProcessReadPage):
    img_ele_attr = 'data-original'
    css_rule = {
        'image_link': '#cp_img img',
    }


class SaveLocally(BaseSaveLocally):
    is_make_read = True
