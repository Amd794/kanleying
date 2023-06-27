# https://coco.tfvisa.com/manhua/shoushinvwangjintianfanpaizilema/

from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_reversal_chapter = True
    is_serial_number = True
    css_rule = {
        'comic_title': '.book-title span',
        'chapter_list': '#chapter-list-1 li',
    }


class ProcessReadPage(BaseProcessReadPage):
    def get_images_url(self, comic_info):
        image_links = re.findall(r'chapterImages = (\[.*?\])', get_response(comic_info['chapter_url']).text, re.S)[0]
        image_links = [image_link.replace('\\', '') for image_link in eval(image_links)]
        return {
            'image_links': image_links,
            'chapter_title': comic_info.get('chapter_title'),
            'comic_title': comic_info.get('comic_title')
        }


class SaveLocally(BaseSaveLocally):
    is_make_read = True


if __name__ == '__main__':
    ProcessReadPage().get_images_url('https://coco.tfvisa.com/manhua/shoushinvwangjintianfanpaizilema/1041740.html')
