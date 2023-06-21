from utils.base import *


class ProcessDetailsPage(BaseProcessDetailsPage):
    is_serial_number = True
    is_reversal_chapter = True
    css_rule = {
        'comic_title': '.title h1',
        'chapter_list': '#chapter-list-1 li',
    }

    def rewrite_comic_title(self, old_title, *args, **kwargs):
        return old_title.replace('漫画', '')


class ProcessReadPage(BaseProcessReadPage):
    def get_images_url(self, comic_info):
        response = get_response(comic_info['chapter_url'])
        chapter_path_regix = 'chapterPath = "(.*?)"'
        chapter_images = eval(re.sub(r'\\', '', re.search('chapterImages = (\[.*?\])', response.text).group(1)))
        chapter_path = re.search(chapter_path_regix, response.text).group(1)
        image_links = [
            f'https://img.wszwhg.net/{chapter_path}' if re.match(r'^http', chapter_path) else chapter_path + i for i
            in chapter_images]
        return {
            'image_links': image_links,
            'chapter_title': comic_info['chapter_title'],
            'comic_title': comic_info['comic_title']
        }


class SaveLocally(BaseSaveLocally):
    pass
