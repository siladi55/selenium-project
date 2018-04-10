#coding=utf-8
import requests
import gevent
import copy
import time
from gevent import monkey; monkey.patch_all()
from lxml import etree
from db.SQLModel import SQLhelper
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
DB = SQLhelper(host='192.168.0.100', user='sa', password='Sa123456', database='vp')
PROXY = {'http': 'http://'+'192.227.112.138:28000',
        'https': 'http://'+'192.227.112.138:28000'}
URL = 'https://www.fakepersongenerator.com/Index/generate'
HEADER = {
        'Host': 'www.fakepersongenerator.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'DNT': '1',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8'
    }

def ua():
    res = DB.search("select top 1 useragent from sys_User_agent_inventroy where useragent_platform = 'PC端浏览器' order by newid()")
    if len(res):
        # print res[0][0]
        return res[0][0]
    else:
        print '数据库获取ua失败，将使用默认UA'
        return 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ' \
               '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

def resp_selector():
    try:
        headers = copy.deepcopy(HEADER)
        headers['User-Agent'] = ua()
        return etree.HTML(requests.get(URL, headers=headers, proxies=PROXY, verify=False, timeout=10).text)
    except:
        print '请求失败，还剩%s次请求机会'%(2-i)
        time.sleep(1)

def parse(s):
    info = {}
    img_xp = '//div[@class="face"]/img/@src'
    name_xp = '//b[@class="click"]/text()'
    gender_xp = '//p[contains(text(),"Gender")]/b/text()'
    birth_xp = '//p[contains(text(),"Birthday")]/b[1]/text()'
    # age_xp = '//p[contains(text(),"Birthday")]/b[2]/text()'
    street_xp = '//p[contains(text(),"Street")]/b/text()'
    CityStateZip_xp = '//p[contains(text(),"City, State, Zip")]/b/text()'
    tel_xp = '//p[contains(text(),"Telephone")]/b/text()'
    mobile_xp = '//p[contains(text(),"Mobile")]/b/text()'
    img = s.xpath(img_xp)
    if len(img):
        info['img_url'] = 'https://www.fakepersongenerator.com' + img[0]
    name = s.xpath(name_xp)
    if len(name):
        info['fullname'] = name[0].replace(u'\xa0', ' ').replace("'", "&acute;")
        nameList = info['fullname'].split(' ')
        info['name'], info['surname'] = nameList[0], nameList[-1]
    gender = s.xpath(gender_xp)
    if len(gender):
        info['gender'] = 0 if 'fe' in gender[0] else 1
    birth = s.xpath(birth_xp)
    if len(birth):
        info['birth_year'], info['birth_month'], info['birth_day'] = birth[0].split('/')
    # age = s.xpath(age_xp)
    # if len(age):
    #     info['age'] = age[0]
    street = s.xpath(street_xp)
    if len(street):
        info['street'] = street[0].replace("'", "&acute;")
    csz = s.xpath(CityStateZip_xp)
    if len(csz):
        info['city'], info['state'], info['zip'] = csz[0].split(', ')
    tel = s.xpath(tel_xp)
    # if len(tel):
    #     info['tel'] = tel[0]
    mob = s.xpath(mobile_xp)
    if len(mob):
        info['mobile'] = mob[0]
    # print 'info-->', info
    return info

def save_to_db(i):
    sql = "insert into sys_profile_inventory(name, surname, fullname, gender, birth_year, birth_month," \
          "birth_day, street, city, state, zip, mobile, img_path, date) values('{0}', '{1}', '{2}', {3}, '{4}'," \
          "'{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', getDate())" \
          "".format(i['name'], i['surname'], i['fullname'], i['gender'], i['birth_year'], i['birth_month'],
                    i['birth_day'], i['street'], i['city'], i['state'], i['zip'], i['mobile'], i['img_url'])
    if DB.run(sql):
        print '入库成功'
    else:
        print '入库失败'


def work_steam():
    """未抓取到，等待60s后再执行"""
    for i in range(3):
        info = parse(resp_selector())
        if len(info):
            save_to_db(info)
            break
        else:
            print '未抓取到数据,等待60s...'
            for i in range(60):
                time.sleep(1)
                print '等待剩余时间：%s' % (60-i)

def main(num):
    """num:需要抓取的条数"""
    g = []
    for i in xrange(num):
        g.append(gevent.spawn(work_steam))
        gevent.sleep(0.01)
    gevent.joinall(g)

if __name__ == '__main__':
    main(30)
