#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from log.log import Logger
L = Logger("task.util")


class Basic(object):
    '''
    setting some basic info requests
    including some module used frequently
    '''

    USER_AGENT = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.53 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.74 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.74 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 1094) AppleWebKit/537.36 (KHTML like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/37.0.2036.33 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11 AlexaToolbar/alxg-3.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11',
        'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.25 (KHTML, like Gecko) Chrome/32.0.2041.55 Safari/537.25',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 4.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52',
    ]

    HEADERS = {
        'Connection': 'keep-alive',
        # 'User-Agent': random.choice(USER_AGENT),
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'DNT': '1',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    }


    # 固定请求头
    HEADER = {
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENT),
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'DNT': '1',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    }

    IP = None
    PORT = None
    PROXY = {
        'http': 'http://%s:%s' % (IP, PORT),
        'https': 'https://%s:%s' % (IP, PORT)
    }


class Date_Transfer(object):
    def __init__(self, cid, raw_date):
        self.cid = cid
        self.raw_date = raw_date

    def two_num_transfer(self, rawno):
        """rawno should > 0, str or int type are both availble """
        try:
            rawno = int(rawno)
            if rawno > 9:
                return str(rawno)
            elif rawno > 0:
                return '0' + str(rawno)
            elif str(rawno ) in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
                return str(rawno)
            else:
                L.error('param rawno should be bigger than 0')
        except Exception, e:
            L.exc(e)

    def month_transfer(self, rawMon):
        m = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        if self.cid in (1, 3):  # US&CA
            month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                     'September', 'October', 'November', 'December']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 2:  # UK
            month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                     'September', 'October', 'November', 'December']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 4:  # Jp
            month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 5:  # De
            month = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September',
                     'Oktober', 'November', 'Dezember']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 6:  # Fr
            month = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre',
                     'octobre', 'novembre', 'décembre']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 7:  # Es
            month = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
                     'octubre', 'noviembre', 'diciembre']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))

        elif self.cid == 8:  # It
            month = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre',
                     'ottobre', 'novembre', 'dicembre']
            if rawMon in month:
                return m[month.index(rawMon)]
            else:
                L.error("No such month[%s] in site:%s" % (rawMon, self.cid))
        else:
            L.error('No such site[%s] in func month_transfer' % self.cid)

    def handle_raw_date(self):
        if self.cid in (1, 3):
            try:
                sl = self.raw_date.strip().split(' ')
                rawmonth = sl[0]
                month = self.month_transfer(rawmonth)
                year = sl[-1].split(', ')[-1]
                rawday = sl[-2].split(',')[0]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 2:
            try:
                sl = self.raw_date.strip().split(' ')
                rawmonth = sl[-2]
                month = self.month_transfer(rawmonth)
                year = sl[-1]
                rawday = sl[-3]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 4:
            try:
                sl = self.raw_date.strip().split('年')
                year = sl[0]
                sl2 = sl[-1].split('月')
                rawmonth = sl2[0]
                month = self.month_transfer(rawmonth)
                rawday = sl2[-1].split('日')[0]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 5:
            try:
                sl = self.raw_date.strip().split(' ')
                year = sl[-1]
                rawmonth = sl[-2]
                month = self.month_transfer(rawmonth)
                rawday = sl[-3].split('.')[0]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 6:
            try:
                sl = self.raw_date.strip().split(' ')
                year = sl[-1]
                rawmonth = sl[-2]
                month = self.month_transfer(rawmonth)
                rawday = sl[-3]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 7:
            try:
                sl = self.raw_date.strip().split(' ')
                year = sl[-1]
                month = self.month_transfer(sl[-3])
                rawday = sl[0]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        elif self.cid == 8:
            try:
                sl = self.raw_date.strip().split(' ')
                year = sl[-1]
                month = self.month_transfer(sl[-2])
                rawday = sl[-3]
                day = self.two_num_transfer(rawday)
                return year + '-' + month + '-' + day
            except Exception, e:
                L.exc(e)
        else:
            L.error('No such site[%s] in func month_transfer' % self.cid)


# 站点编码
def cidTransfer(con):
    if con == 'www.amazon.com':
        return 1
    elif con == 'www.amazon.co.uk':
        return 2
    elif con == 'www.amazon.ca':
        return 3
    elif con == 'www.amazon.co.jp':
        return 4
    elif con == 'www.amazon.de':
        return 5
    elif con == 'www.amazon.fr':
        return 6
    elif con == 'www.amazon.es':
        return 7
    elif con == 'www.amazon.it':
        return 8
    elif con == 1 or con == '1':
        return 'www.amazon.com'
    elif con == 2 or con == '2':
        return 'www.amazon.co.uk'
    elif con == 3 or con == '3':
        return 'www.amazon.ca'
    elif con == 4 or con == '4':
        return 'www.amazon.co.jp'
    elif con == 5 or con == '5':
        return 'www.amazon.de'
    elif con == 6 or con == '6':
        return 'www.amazon.fr'
    elif con == 7 or con == '7':
        return 'www.amazon.es'
    elif con == 8 or con == '8':
        return 'www.amazon.it'
    else:
        return




