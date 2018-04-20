#coding=utf-8
import time
import random
import logging
import os


class SysEnvConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.guid = ''
        self.mac = ''
        self.sys_lang = ''
        self.cid = 1
        self.screen_px = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'guid': self.guid = kwargs[k]
            if k == 'sys_lang': self.sys_lang = kwargs[k]
            if k == 'mac': self.mac = kwargs[k]
            if k == 'cid': self.cid = kwargs[k]
            if k == 'screen_px': self.screen_px = kwargs[k]

class BrowserConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.execute_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.timeout = 60
        self.user_agent = ''
        # self.proxy = '192.168.0.5:26661'  # ip:port
        self.proxy = ''  # ip:port or ip@port@user@pw
        self.showImg = True
        self.font = 'en-us'
        self.acpt_lang = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'user_agent': self.user_agent = kwargs[k]
            if k == 'proxy': self.proxy = kwargs[k]
            if k == 'font': self.font = kwargs[k]
            if k == 'acpt_lang': self.acpt_lang = kwargs[k]

class DriverConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.stay_time = (2, 3)
        self.waitime = 30
        self.page_offset = 500
        self.page_move_rate = (5, 10)
        self.rand_move_lenth = (100, 600)
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'stay_time': self.stay_time = kwargs[k]
            if k == 'waitime': self.waitime = kwargs[k]
            if k == 'page_offset': self.page_offset = kwargs[k]
            if k == 'page_move_rate': self.page_move_rate = kwargs[k]
            if k == 'rand_move_lenth': self.rand_move_lenth = kwargs[k]


class RegistConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.guid = ''
        self.yourname = 'Kev'
        self.user = 'chenj@qq.com'
        self.pw = 'asdf123456'
        self.cid = 1
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'guid': self.guid = kwargs[k]
            if k == 'user': self.user = r'' + kwargs[k]
            if k == 'pw': self.pw = kwargs[k]
            if k == 'cid': self.cid = kwargs[k]
            if k == 'yourname': self.yourname = kwargs[k]


class AddrConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.guid = ''
        self.user = ''
        self.addr_cty = 1
        self.fullname = ''
        self.streetaddr = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.phoneNo = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'guid': self.guid = kwargs[k]
            if k == 'user': self.user = r'' + kwargs[k]
            if k == 'addr_cty': self.addr_cty = kwargs[k]
            if k == 'fullname': self.fullname = kwargs[k]
            if k == 'streetaddr': self.streetaddr = kwargs[k]
            if k == 'city': self.city = kwargs[k]
            if k == 'state': self.state = kwargs[k]
            if k == 'zip_code': self.zip_code = kwargs[k]
            if k == 'phoneNo': self.phoneNo = kwargs[k]


class ProfileConf(object):
    def __init__(self, param_dict, **kwargs):
        self.guid = ''
        self.user = ''
        self.imgPath = r'F:\SpiderProgram\AMZ_shuadan\1.jpg'
        self.bio = 'I am someone you like'
        self.fb = 'www.fb.com'
        self.twitter = 'www.twitter.com'
        self.youtube = 'www.youtube.com'
        self.pint = 'www.pint.com'
        self.instagram = 'www.instagram.com'
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'guid': self.guid = kwargs[k]
            if k == 'user': self.user = r'' + kwargs[k]
            if k == 'imgPath': self.imgPath = r'' + kwargs[k]
            if k == 'bio': self.bio = kwargs[k]
            if k == 'fb': self.fb = kwargs[k]
            if k == 'twitter': self.twitter = kwargs[k]
            if k == 'youtube': self.youtube = kwargs[k]
            if k == 'pint': self.pint = kwargs[k]
            if k == 'instagram': self.instagram = kwargs[k]


class LoginConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.user = ''
        self.pw = ''
        self.cid = 1
        self.name = ''
        self.task_guid = ''

        self.by_click = True
        if self.by_click:
            self.host = 'pop.rurumail.com'
            self.port = 110
            self.wait_mail = 6   # 10s/loop
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'user': self.user = r'' + kwargs[k]
            if k == 'pw': self.pw = kwargs[k]
            if k == 'cid': self.cid = kwargs[k]
            if k == 'name': self.name = kwargs[k]
            if k == 'task_guid': self.task_guid = kwargs[k]


class SearchConf(object):
    def __init__(self, param_dict, **kwargs):
        self.task_guid = ''
        self.user = ''
        self.cid = 1
        self.asin = ''
        self.kw = ''
        self.option_value = ""
        self.cata = ''
        self.search_price = ()
        self.search_page = 5
        self.ignore_sponsored = 1
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'task_guid': self.task_guid = kwargs[k]
            if k == 'user': self.user = kwargs[k]
            if k == 'cid': self.cid = kwargs[k]
            if k == 'asin': self.asin = kwargs[k]
            if k == 'kw': self.kw = kwargs[k]
            if k == 'option_value': self.option_value = kwargs[k]
            if k == 'cata': self.cata = kwargs[k]
            if k == 'search_price': self.search_price = kwargs[k]
            if k == 'search_page': self.search_page = kwargs[k]
            if k == 'ignore_sponsored': self.ignore_sponsored = kwargs[k]


class TaskGuid(object):
    def __init__(self, param_dict=None, **kwargs):
        self.task_guid = ''
        self.task_id = None
        self.user = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'task_guid': self.task_guid = kwargs[k]
            if k == 'task_id': self.task_id = kwargs[k]
            if k == 'user': self.user = kwargs[k]


class TrafficActConf(object):
    """{1:add-to-cart购物车， 2:add-to-list清单，3:评论，4:问答}"""
    def __init__(self, param_dict=None, **kwargs):
        # assert isinstance(kwargs, dict) and set(kwargs.keys()).issubset(self.__dict__.keys())
        self.user = ''
        self.review_title = ''
        self.review_author = ''
        self.review_help = None
        self.question_id = None
        self.answerer_id = None
        self.answer_help = None
        self.vote = None
        self.task_guid = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'user': self.user = kwargs[k]
            if k == 'review_title': self.review_title = kwargs[k]
            if k == 'review_author': self.review_author = kwargs[k]
            if k == 'review_help': self.review_help = kwargs[k]
            if k == 'question_id': self.question_id = kwargs[k]
            if k == 'answerer_id': self.answerer_id = kwargs[k]
            if k == 'answer_help': self.answer_help = kwargs[k]
            if k == 'vote': self.vote = kwargs[k]
            if k == 'task_guid': self.task_guid = kwargs[k]


class ShoppingConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.task_guid = ''
        self.user = None
        self.pw = None
        self.cid = None
        self.buy_cart = None
        self.shop_name = None
        self.shop_id = None
        self.fba = None
        self.newAddrGuid = None
        self.ccard_guid = None
        self.giftcard_guid = None
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'task_guid': self.task_guid = kwargs[k]
            if k == 'user': self.user = kwargs[k]
            if k == 'pw': self.pw = kwargs[k]
            if k == 'cid': self.cid = kwargs[k]
            if k == 'buy_cart': self.buy_cart = kwargs[k]
            if k == 'shop_name': self.shop_name = kwargs[k]
            if k == 'shop_id': self.shop_id = kwargs[k]
            if k == 'fba': self.fba = kwargs[k]  #1:卖家自发货，2FBA
            if k == 'newAddrGuid': self.newAddrGuid = kwargs[k]
            if k == 'ccard_guid': self.ccard_guid = kwargs[k]
            if k == 'giftcard_guid': self.giftcard_guid = kwargs[k]

class CardConf(object):
    def __init__(self, param_dict=None, **kwargs):
        self.gift_code = ''
        self.ccname = ''
        self.ccNo = ''
        self.exp_mon = ''
        self.exp_year = ''
        if param_dict:
            self.update(param_dict)
        else:
            self.update(kwargs)

    def update(self, kwargs):
        for k in kwargs:
            if k == 'gift_code': self.gift_code = kwargs[k]
            if k == 'ccname': self.ccname = kwargs[k]
            if k == 'ccNo': self.ccNo = kwargs[k]
            if k == 'exp_mon': self.exp_mon = kwargs[k]
            if k == 'exp_year': self.exp_year = self.convert_year(kwargs[k])

    def convert_year(self, year):
        year = int(year)
        cur_year = int(time.strftime("%Y"))
        if 0 <= (year - cur_year) <= 20:
            for i in range(21):
                if cur_year == year:
                    return i+1
                cur_year += 1
        else:
            print '信用卡有效期年限无效'
            return 0


if __name__ == '__main__':
    # a = {'option': 2, 'review_title': 'Good', 'answer_help': 1}
    # d = TrafficActConf(a)
    # print d.__dict__
    # print vars(CardConf())
    b = CardConf()
    print b.convert_year('2025')