# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2020/3/28 19:22
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794


import asyncio
import datetime
import os
import re
import threading
import warnings
from typing import NoReturn

import aiofiles
import aiohttp
import requests
from PIL import Image, ImageFont, ImageDraw
from fake_useragent import UserAgent

# from conf import global_settings
from conf import settings

warnings.simplefilter('ignore', RuntimeWarning)
requests.packages.urllib3.disable_warnings()
glock = threading.Lock()
from utils.comic_tools import Util


def generate_alternate_images(text, img_save_path):
    """
    # todo 生成替换的图片
    """
    Util.cre_folder(os.path.dirname(img_save_path))
    font_size = 24
    liens = text.split('\n')
    im = Image.new("RGB", (len(text) * 12, len(liens) * (font_size + 5)), '#fff')
    dr = ImageDraw.Draw(im)
    font_path = r"C:\Windows\Fonts\STKAITI.TTF"
    font = ImageFont.truetype(font_path, font_size)
    dr.text((0, 0), text, font=font, fill="blue")
    im.save(img_save_path)


def cre_a_repair_img_script(file_path):
    """
    # todo 创建修复图片的脚本
    """
    if os.path.exists(file_path) and 'error_urls.txt' in os.listdir(file_path):
        print('-------------生成图片修复文件--------------')
        from shutil import copyfile, SameFileError
        try:
            copyfile('../utils/try_to_fix.py', os.path.join(file_path, 'try_to_fix.py'))
        except SameFileError:
            print('-------------脚本文件已经存在--------------')


def req_headers(src_lnk, headers):
    """
    # todo 获取请求头
    """

    def referer_param(src_lnk):
        referer_obj = {
            'qinqinmh': 'https://www.qinqinmh.com/',
            'piddd': 'https://www.qinqinmh.com/',
            'manhua.acimg': '',
        }
        return referer_obj.get(
            next(
                filter(
                    lambda key: key in src_lnk,
                    referer_obj
                ),
                None
            ),
            src_lnk)

    def ua_param(src_lnk):
        if re.search(fr'https?://(?:\w+\.)?({"|".join(settings.use_pc_ua)})\.\w+/', src_lnk):
            return UserAgent(path='../res/fake_useragent_0.1.11.json').random
        return 'Mozilla/5.0 (Linux; Android 7.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36 Edg/87.0.664.47'

    if not headers:
        headers = {
            'User-Agent': ua_param(src_lnk),
            'referer': referer_param(src_lnk),
            # 不缓存
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
        }

    return headers


def handle_lnk(src_lnk: str):
    """
    # todo 处理源链接
    """
    lnk_obj = {
    }
    for key in lnk_obj:
        if key in src_lnk:
            src_lnk = lnk_obj.get(key)

    return src_lnk


def get_response(url: str, error_file_path: str = '.', max_count: int = 3, timeout: int = 60,
                 encoding: str = 'utf-8', name: str = '', header=None) -> object:
    """
    #   todo 获取返回的response
    """
    global response
    if header is None:
        header = {}
    count = 0
    # proxy = requests.get("http://192.168.1.103:15010/get/?type=https").json()['proxy']
    # print(f'{url} 使用了代理IP {proxy}'.center(80, '-'))
    while count < max_count:
        try:
            response = requests.get(url=url, headers=req_headers(handle_lnk(url), header), verify=False,
                                    timeout=timeout,
                                    # proxies={
                                    #     "https": f"http://{proxy}", }
                                    )
            response.raise_for_status()  # 如果status_code不是200, 产生异常requests .HTTPError
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException:
            print(
                f'\033[22;33;m{url} {response} {name}连接超时, 正在进行第{count + 1}次连接重试, {timeout}秒超时重连\033[m')
            count += 1
    else:
        print(f'\033[22;31;m{url}重试{max_count}次后依然连接失败, 放弃连接...\033[m')
        Util.cre_folder(error_file_path)
        glock.acquire()
        with open(os.path.join(error_file_path, 'error_urls.txt'), 'a') as f:
            f.write(url + ' ' + name + '\n')
        glock.release()
        return None


class AsyncDown:
    def __init__(self, save_path, headers):
        self.save_path = save_path
        self.headers = headers

    async def async_download(self, session, index_url):
        def log_err_lnk(bad_lnk, file_path, index):
            generate_alternate_images(f'{bad_lnk}', f'{os.path.join(file_path, str(index))}.jpg')
            with open(f'{file_path}/error_urls.txt', 'a') as f:
                f.write(f'{bad_lnk} {index}.jpg\n')

        index, url = index_url
        try:
            async with session.get(handle_lnk(url), verify_ssl=False,
                                   headers=req_headers(handle_lnk(url), self.headers),
                                   timeout=60) as response:
                Util.cre_folder(self.save_path)
                print(f'正在下载：{response.status} {handle_lnk(url)} ---> {index}.jpg')
                if response.status == 200:
                    async with aiofiles.open(f'{self.save_path}/{index}.jpg', 'wb') as fw:
                        try:
                            while True:
                                chunk = await response.content.read()
                                if not chunk:
                                    break
                                await fw.write(chunk)
                        except TypeError:
                            log_err_lnk(handle_lnk(url), self.save_path, index)
                else:
                    raise IOError
        except (aiohttp.ClientConnectorError,
                aiohttp.ServerDisconnectedError,
                asyncio.exceptions.TimeoutError,
                aiohttp.InvalidURL,
                aiohttp.ClientOSError,
                IOError) as e:
            print(f"#ERROR {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {handle_lnk(url)} {index}.jpg {e}")
            log_err_lnk(handle_lnk(url), self.save_path, index)
            return None

    async def enqueue(self, img_lnk_a: list[str]) -> NoReturn:
        """
        :param img_lnk_a: 一个只包含图片链接的列
        :return:
        """
        async with aiohttp.ClientSession() as session:
            tasks = list(
                map(
                    lambda index_url: asyncio.create_task(self.async_download(session, index_url)),
                    enumerate(img_lnk_a) if isinstance(img_lnk_a[0], str) else img_lnk_a
                )
            )
            await asyncio.wait(tasks)
        cre_a_repair_img_script(self.save_path)


def async_down(image_list, file_path=os.getcwd(), headers=None):
    loop = asyncio.get_event_loop()
    task_queue = AsyncDown(file_path, headers).enqueue(image_list)
    loop.run_until_complete(task_queue)


if __name__ == '__main__':
    imgs = \
        [
            'https://awjktuh.skxuzescyufn.hath.network:32399/h/170b4379697c3ffb5fb9d99e1ea35930a93ff733-272914-720-2803-jpg/keystamp=1667135700-050e853194;fileindex=85880407;xres=org/015_001.jpg',
            'https://bdgwlgq.llzatnodtbok.hath.network/h/4bc6b1294354d8ed8b1c4f656e5f86d15378477e-256293-720-2804-jpg/keystamp=1667135700-a670478675;fileindex=85880408;xres=org/015_002.jpg',
            'https://gdprtko.wdofttbdoqvc.hath.network:8080/h/b8b4f95594cdc015528fba83aaa5dcb54c8bba61-232854-720-2803-jpg/keystamp=1667135700-2bc5d370bd;fileindex=85880409;xres=org/015_003.jpg',
            'https://svmdchz.cxzapmxcdkgw.hath.network/h/528cfeb96a60bcba6e3564ca25794fc21432eca4-243363-720-2803-jpg/keystamp=1667135700-24c0103e78;fileindex=85880411;xres=org/015_004.jpg',
            'https://jiqzssr.pkyrevyniviv.hath.network/h/8e80e8321d06b8d0311194c7b9a605aed340210a-198524-720-2804-jpg/keystamp=1667135700-d6e0824d5c;fileindex=85880412;xres=org/015_005.jpg',
            'https://vxozpqf.htoqbgqxsjls.hath.network/h/27ea5fdf84a73e522523a85e4abad47ca4017503-290142-720-2803-jpg/keystamp=1667135700-b6957a066a;fileindex=85880413;xres=org/015_006.jpg',
            'https://yolxley.paietqzvwvlo.hath.network/h/f9834c7b49f1714348ab9829595088ede68573e7-219162-720-2789-jpg/keystamp=1667135700-c9f10530b4;fileindex=85880414;xres=org/015_007.jpg',
            'https://qoiojdw.fubgwmtkiemp.hath.network:6200/h/90e9a1a83ec8dc135a1af12a32c09794ac8b2261-210298-720-2789-jpg/keystamp=1667135700-457b1ef00a;fileindex=85880415;xres=org/015_008.jpg',
            'https://znluglo.reffwjnksaft.hath.network/h/ba449149870df3a9210ff6f20118207ac57770c3-245458-720-2789-jpg/keystamp=1667135700-a5da2bd802;fileindex=85880417;xres=org/015_009.jpg',
            'https://vpeevvv.ikqytlotkgmy.hath.network:23567/h/58fcb48ac9775a71d1bcf26ccbed288b2068b26a-286018-720-2789-jpg/keystamp=1667135700-2b93a9193f;fileindex=85880418;xres=org/015_010.jpg',
            'https://vkiikqn.gnwqvdwfgvgz.hath.network:61500/h/22007fbab5b89987ead68044bfefd9aafdc8e159-238586-720-2789-jpg/keystamp=1667135700-7159a0e771;fileindex=85880419;xres=org/015_011.jpg',
            'https://ejqukoz.reffwjnksaft.hath.network/h/720ee4e30e78323778d8e811e785e39f4789e96b-272921-720-2789-jpg/keystamp=1667135700-22e61e2715;fileindex=85880420;xres=org/015_012.jpg',
            'https://mtrvtfw.vudsewkvmxth.hath.network/h/afd4eab62d199cd4fbf89732fa38b1523277bedc-261736-720-2803-jpg/keystamp=1667135700-fb92f1a66c;fileindex=85880421;xres=org/015_013.jpg',
            'https://gqoubkl.reffwjnksaft.hath.network/h/6356a7e3c32fc2489c1d2f448a65bb67b2df496b-285170-720-2804-jpg/keystamp=1667135700-9eacb44d76;fileindex=85880423;xres=org/015_014.jpg',
            'https://dnmrtrf.wdofttbdoqvc.hath.network:11111/h/b4e61f534b706e445a961c1a7ff648cef47c905b-245376-720-2803-jpg/keystamp=1667135700-d1716bac51;fileindex=85880424;xres=org/015_015.jpg',
            'https://gmbkgjv.nxyhwzrrtkud.hath.network/h/6c6a0d516bea946a9bd4b3a4537e8e89c0fac7e9-211823-720-2803-jpg/keystamp=1667135700-81dc5c2168;fileindex=85880425;xres=org/015_016.jpg',
            'https://fmoarub.pwadjsofubud.hath.network:2688/h/072b9e95251944c715380f7a595f9cce35c09b42-230158-720-2804-jpg/keystamp=1667135700-843df200cb;fileindex=85880426;xres=org/015_017.jpg',
            'https://wrupnrz.pkyrevyniviv.hath.network/h/5f89b1d5e4609cfd287b64abe8b4e91733d16c19-197833-720-2803-jpg/keystamp=1667135700-ea315f25fd;fileindex=85880428;xres=org/015_018.jpg',
            'https://iiqtxxa.phonlvdewsbz.hath.network:32323/h/02ea6ea4b7d05e48e8c0041c6e12b49e92bc0951-199819-720-2082-jpg/keystamp=1667135700-41c0ece494;fileindex=85880429;xres=org/015_019.jpg',
            'https://slvvyah.xuukuslterjz.hath.network:27128/h/a5b3a1b516a8a3ee9522750b1dede0a5f6db8498-168307-720-2081-jpg/keystamp=1667135700-b24934d8a5;fileindex=85880430;xres=org/015_020.jpg',
            'https://hbxowci.pihnbhkoqoas.hath.network/h/53a0cbfac96f7fa4d7dc1a74820b4ee01976e879-98511-720-2082-jpg/keystamp=1667135700-b641a10541;fileindex=85880431;xres=org/015_021.jpg']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
    }
    async_down(imgs, '../test')
