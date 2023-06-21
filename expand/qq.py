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
        headers = {
            'cookie': 'RK=sByF9XM+4a; ptcz=81f20f9c32d800ab43df7e3aebc24015d70c15704bc46ec6e90124d3fd103403; tvfe_boss_uuid=fe3ff18e2a9c166b; pgv_pvid=4368074832; o_cookie=2952277346; gr_user_id=3062b53c-b3e0-444d-ba53-7bfe2fc8b56d; _txjk_whl_uuid_aa5wayli=10992aa3a049443e8ad18780512c0b28; ts_uid=2541005042; ptui_loginuin=2952277346; ied_qq=o2952277346; eas_sid=o1T682c916r0i741n938j3h4T1; theme=white; roastState=2; readLastRecord=[]; pgv_info=ssid=s8621565400; Hm_lvt_f179d8d1a7d9619f10734edb75d482c4=1631429115,1631938474,1632023425; uin=o2952277346; _qpsvr_localtk=0.8086994936469347; login_type=4; open_id=B281DD9D8BD22EFBB28D6F073D0A1B4E; access_token=4A65B8BE9B4106DB67311A95DAA4BA25; readRecord=[[638870,"从今天开始当城主",60,"049 米娜的危机",53],[643504,"绝世战魂","496","第336话 逆天元神晋级",337],[642290,"妙手狂医","732","第223话 狠狠的打",229],[647667,"我有九个女徒弟","463","第206话 第九城的恩赐",213],[648635,"武神当世","805","第116话 献宝",118],[621058,"我是大神仙","640","第四三零话·收买人心",445],[624570,"传武","738","第二卷 140 灌江口二郎！",269],[645919,"沧元图","705","战前准备",178],[628970,"元尊","747","第343话：强者云集（下）",704],[622498,"星武神诀","795","第485话",492],[546493,"中华神医",511,"第488话 换助手？",494],[533395,"妖神记","683","第345话 写了好多字（下）",625],[530955,"戒魔人","868","第779话 炼化完美创世石",781],[505430,"航海王","1090","第1025话 双龙图",1025],[642370,"失业魔王",1,"序章",1]]; ts_last=ac.qq.com/ComicView/index/id/638870/cid/60; Hm_lpvt_f179d8d1a7d9619f10734edb75d482c4=1632113989'.encode(
                'utf-8')
        }
        response = get_response(comic_info['chapter_url'], header=headers, encoding='utf-8')
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
    pass
