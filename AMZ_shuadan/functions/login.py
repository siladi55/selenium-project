#coding=utf-8
import sys
import browser as bo
from util import CidTransfer, rand_stay
from db.SQLModel import Record2DB
from logs.log import Logger
from setting import *
reload(sys)
sys.setdefaultencoding('utf-8')
L = Logger(__file__)
Rdb = Record2DB()


class Login(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf
        self.url = 'https://' + CidTransfer(conf.cid).value

    def login_with_cookie(self):
        print '3', self.conf.task_guid
        self.d.request(self.url)
        self.d.to_first_handler()
        self.d.delete_cookies()
        if self.addCookies():
            self.d.refresh_page()
            if self.conf.cid in (2, 5):
                user_xpath = '//a[@id="nav-link-yourAccount"]/span[contains(text(), "%s")]' % self.conf.name
            elif self.conf.cid in (1, 3, 4, 6, 7, 8):
                user_xpath = '//a[@id="nav-link-accountList"]/span[contains(text(), "%s")]' % self.conf.name
            else:
                user_xpath = ''
                L.error('Wrong params "contry id": %s' % self.conf.cid)
            # print user_xpath, type(user_xpath)
            if self.d.is_element_exist(user_xpath):
                L.info('带cookie账号登录成功')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '带cookie登录成功')
                bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                return True
            else:
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '带cookie登录失败')
                L.error('带cookie账号登录失败')
                return False
                # return self.login_by_click()
        else:
            L.error('<login> cookie添加失败, 代理网速太慢')
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录失败, 代理网速太慢')
            return False

    def login_by_click(self):
        login_xpath = str()
        if self.conf.cid in (2, 5):
            login_xpath = '//a[@id="nav-link-yourAccount"]'
        elif self.conf.cid in (1, 3, 4, 6, 7, 8):
            login_xpath = '//a[@id="nav-link-accountList"]'
        u_xpath = '//input[@id="ap_email"]'
        p_xpath = '//input[@id="ap_password"]'
        ctn = '//input[@id="continue"]'
        sub_xpath = '//input[@id="signInSubmit"]'
        self.d.request(self.url)
        self.d.to_first_handler()
        # self.d.delete_cookies()
        # self.addCookies()
        """
        self.d.wait_clickable(login_xpath)
        self.d.rand_move()
        self.d.click_opt(login_xpath)
        if not self.d.is_element_exist(u_xpath) and self.d.is_element_exist(p_xpath):
            self.d.wait_clickable(sub_xpath)
            self.d.send_key(p_xpath, self.conf.pw)
            self.d.click_opt(sub_xpath)
            if self.d.is_element_exist(sub_xpath):
                L.error('<login> 登录失败, 请检查账号密码和cookie')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录失败, 请检查账号密码')
                return False
            else:
                bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录成功')
                return True
        else:
            self.d.wait(u_xpath)
            self.d.send_key(u_xpath, self.conf.user)
            if self.d.is_element_exist(p_xpath):
                self.d.wait_clickable(sub_xpath)
                self.d.send_key(p_xpath, self.conf.pw)
                self.d.click_opt(sub_xpath)
            else:
                self.d.wait_clickable(ctn)
                self.d.click_opt(ctn)
                self.d.wait(p_xpath)
                self.d.wait_clickable(sub_xpath)
                self.d.send_key(p_xpath, self.conf.pw)
                self.d.click_opt(sub_xpath)
            # 判断是否登录成功，如果成功则保存cookies
            if self.d.is_element_exist('//input[@id="continue"]'):
                L.error('<login> 登录失败，需要邮箱接收验证码登录')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录失败，账号登录环境与上次不同，需要邮箱验证')
                return False
            else:
                bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录成功')
                return True
        # else:
        #     return False
        """
    def addCookies(self):
        try:
            table = 'account_cookies'
            field = ['cookies']
            where = "account='%s'" % self.conf.user
            ck = Rdb.search_(table, field, where)
            if len(ck):
                cookie = ck[0][0].replace("&acute;", "'")
                # print type(eval(cookie)), eval(cookie)
                if self.d.add_cookies_to_bs(eval(cookie)):
                    L.info('浏览器cookie设置成功')
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '浏览器Cookie 设置成功')
                    return True
                else:
                    L.info('浏览器cookie设置成功')
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '浏览器Cookie 设置超时导致失败')
                    return False
            else:
                L.error("未找到账号%s登录的cookie" % self.conf.user)
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '浏览器Cookie 设置失败，Cookie没查到')
                return False
        except:
            L.exc('浏览器Cookie设置失败')
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '浏览器Cookie 设置失败(请检查操作节点)')
            return False


if __name__ == '__main__':

    pass

