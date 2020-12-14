import base64
import re

import requests
from pyquery import PyQuery

from kanleying import Comic


def get_info(detail_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    try:
        res = requests.get(detail_url, headers=headers).text
        print(res)
        nonce = re.findall('window\["n.*?e"\]\s=\s(.*?);', res)[1]
        data = re.findall('var DATA.*?\'(.*?)\'', res)[0]
        chapter = re.findall('title-comicHeading\">(.*?)<', res)[0].replace(' ', '')
        chapters = PyQuery(res)('#catalogueList li .tool_chapters_list_title').text().split()
        chapter = str(chapters.index(chapter) + 1).rjust(3, '0') + chapter
        chapters = [str(chapters.index(chapter) + 1).rjust(3, '0') + chapter for chapter in chapters]
        name = re.findall('<title>《(.*?)》', res)[0]
        return (nonce, data, chapter, chapters, name)
    except Exception as er:
        print(detail_url, er)


def __parse_img(nonce, data):
    T = [i for i in data]
    N = re.findall('\d+[a-zA-Z]+', nonce)
    length = len(N)
    while length:
        locate = int(re.findall('\d+', N[length - 1])[0]) & 255
        string = re.sub('\d+', '', N[length - 1])
        del T[locate:locate + len(string)]
        length -= 1
    T = ''.join(T)
    return base64.b64decode(T.encode())


def ac_qq(detail_url):
    nonce, data, chapter, chapters, name = get_info(detail_url)
    d = __parse_img(nonce, data)
    t = re.findall('"url":"(.*?)"', str(d))
    l = [str(i).replace(r'\\', '') for i in t]
    print(l)
    Comic.download_images({'images_url': l, 'chapter': chapter, 'comic_title': name}, chapters)


if __name__ == '__main__':
    urls = [
        'https://ac.qq.com/ComicView/index/id/635142/cid/3',
    ]
    for url in urls:
        ac_qq(url)
