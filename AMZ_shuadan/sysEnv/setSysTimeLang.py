#coding=utf-8
import requests
import pytz
import struct
import datetime
import win32api
from lxml import etree
from logs.log import Logger
L = Logger(__file__)

def crawl_time(cid):
    map_ = {0:'beijing', 1:'washington-dc', 2:'london', 3:'ottawa',
            4:'tokyo', 5:'berlin', 6:'paris', 7:'madrid', 8:'rome', 9:'canberra'}
    url = 'http://time.tianqi.com/%s/' % map_[cid]
    header = {
        "Host": "time.tianqi.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Upgrade-Insecure-Requests": '1',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "DNT": '1',
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8"}
    try:
        resp = requests.get(url, headers=header)
        sele = etree.HTML(resp.text)
        xp = '//p[@id="clock"]/text()'
        t = sele.xpath(xp)
        return t[0].encode('utf-8') if len(t) else None
    except Exception, e:
        L.exc(e)

def setSysTime(cid):
    times = crawl_time(cid)
    assert times is not None, "世界时间获取失败，请检查"
    year = times[0:4]
    month = times[7:9]
    day = times[12:14]
    time = times[28:]
    today = year + '-' + month + '-' + day + ' ' + time
    now = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
    now = now - datetime.timedelta(hours=8)
    weekday = now.weekday()
    se = win32api.SetSystemTime(now.year, now.month, weekday, now.day, now.hour, now.minute, now.second, 0)


def setScreenPx(width=1920, height=1080):
    width, height = int(width), int(height)
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsHeight = height
    dm.PelsWidth = width
    dm.BitsPerPel = 32
    dm.DisplayFixedOutput = 0
    win32api.ChangeDisplaySettings(dm, 0)


if __name__ == '__main__':
    # getTime()
    setSysTime(0)
    setScreenPx()
    # print crawl_time(3)
    # def CK():
    #     a = '''[{&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;a-ogbcbff&acute;, &acute;value&acute;: &acute;1&acute;, &acute;expiry&acute;: 1521641082.107667}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;skin&acute;, &acute;value&acute;: &acute;noskin&acute;}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;session-id-time&acute;, &acute;value&acute;: &acute;2082787201l&acute;, &acute;expiry&acute;: 2082742867.004182}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;ubid-main&acute;, &acute;value&acute;: &acute;134-4060264-7081868&acute;, &acute;expiry&acute;: 2082742865.014961}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;session-token&acute;, &acute;value&acute;: &acute;"/ywj8zXcGjQQAHNCs1wxUzGzYig+buFTpSG8Widz7RZ358l1Brh+BzCoDhNUqq+4utsU3gSqJTOct6J3M8//Rd/ipViUsAAVHOLY0x85oCxvzxone45J0brYAzBXlWONaCZjPuj/5+lE8M0scRRzqN8cEd/t68hVqkmQgCdGHmab4+F6fGMs24LlvtSmrhj4M67aLpcIaC0bSP5TaAV37Tq8d04sLYf4mBonbGLUZlB4aGH8c/pHjvcmQSiHdHs43AezCzbDxs1xupOh5r57rQ=="&acute;, &acute;expiry&acute;: 2082742867.004199}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;session-id&acute;, &acute;value&acute;: &acute;135-1658598-0444344&acute;, &acute;expiry&acute;: 2082742867.004136}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;x-main&acute;, &acute;value&acute;: &acute;"qe0?3UpWwDVYLAO5H@K2XhpXwFDZXWGnxy3?zGciaaPUkTLPjMyklhfIePpT0BlX"&acute;, &acute;expiry&acute;: 2152360243.107785}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;at-main&acute;, &acute;value&acute;: &acute;Atza|IwEBIEwa7PhRQNeGCvTg5t9OsEZ1NYspnfrWvZCfgJ3BOsU9_F9OZus-1iz758eYJUSGbxC9RU5iQt05t3zzTjNv1bXnJOapDxrfAhIVVmiS6QSVJ1aGThmblStshwlAKQ2Fsr2hflNVEcQG5YPUx6MD18J8aqcMWwrG_T5jPjotRByqOLkOmXdXJBPN48I0sQivkbKL09liggXMGnOxpYVCDo1e_AkZ6VZcKiPr-6_jxHVtVIQftBwdhdKcU9RFIL9Z1YcfnBO9VfElt2Ud1iVgFwiqFeC5dbNtfz6S1qxCIUCLhaYbixq53EDwmETcfaXUo6FJtr1d-_Bc8-JghYKTZIW8TSnt0O5xrKoNnYHfWBOtBovrQbMtUntjToDaMdjx8MXzk8Oo2igTq14NbMoN__pK&acute;, &acute;expiry&acute;: 2152360243.107801}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;sess-at-main&acute;, &acute;value&acute;: &acute;"RwmEqx06kSvmTt9wSpM6J2sIiQ6oIvu79R/G4B47zGY="&acute;, &acute;expiry&acute;: 2152360243.107824}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;sst-main&acute;, &acute;value&acute;: &acute;Sst1|PQE380kpAtR6vW35JYOP3aPuCFF6mfpiGRp7w-uAP00zJ0EVlaQKoek_K61PnNOCmduRfoOsV70qMO4Elm2Nxrlx3v346PQAx5g7Vbo8SEUXNczT5Iq2Ums1WfrJbYoXwoKFqRafD2mGZT75ivUIxEV8Rkf1x2kob4RYnv7vzF-kgsiTZkkxZmVo0SX6ucb4Pt2OE0OKkn95W0pkR2EWAPzjz9Z2nb7uPO8bGUwewDOjW-LHTUxGaiRMoBXI5rJ9ccoGS5iCujio6cEr6c5I286elA&acute;, &acute;expiry&acute;: 2152360243.107837}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;www.amazon.com&acute;, &acute;name&acute;: &acute;csm-hit&acute;, &acute;value&acute;: &acute;tb:s-E9XXWYKHPCF84CD3Z4S8|1521640243909&adb:adblk_no&acute;, &acute;expiry&acute;: 1522245044}, {&acute;path&acute;: &acute;/&acute;, &acute;domain&acute;: &acute;.amazon.com&acute;, &acute;name&acute;: &acute;x-wl-uid&acute;, &acute;value&acute;: &acute;1j55flGgeGmp3TerS8iyMbJD1pUiE+4MysgsyDskehYCCxVJU9uLdn+4aqpYZys4KnCO2JLHsv+HCUZ0JuszeHe4Za4MOUOUqfsC+1odete0TEBdaWPPO5/+EvqWQMyy+ZA8ncuyCUHg=&acute;, &acute;expiry&acute;: 2082742865.481662}]'''
    #     a = a.replace('&acute;',"'").replace('[', '').replace(']', '').replace('\'\"', "'").replace('}, ', '}<>')
    #     b = a.split("<>")
    #     import json
    #     for i in range(len(b)):
    #         b[i] = eval(b[i])
    #         print type(b[i])
    #     c = json.dumps(b, ensure_ascii=False)
    #     print c
    #     print type(c)

    # def timeStamp():
    #     import time
    #     timeStamp = 1511423457
    #     timeArray = time.localtime(timeStamp)
    #     otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    #     print otherStyleTime
    # timeStamp()