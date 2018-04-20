#coding=utf-8
import sys
import browser as bo
import time
from util import CidTransfer
from db.SQLModel import Record2DB
from logs.log import Logger
from mail_auth.mailauth_handler import MailServer
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
            if self.d.is_element_exist(user_xpath):
                L.info('带cookie账号登录成功')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '带cookie登录成功')
                bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                return True
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '带cookie登录失败')
                L.error('带cookie账号登录失败')
                return False
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
        self.d.wait_clickable(login_xpath)
        self.d.rand_move()
        self.d.click_opt(login_xpath)
        if not self.d.is_element_exist(u_xpath) and self.d.is_element_exist(p_xpath):
            self.d.wait_clickable(sub_xpath)
            self.d.send_key(p_xpath, self.conf.pw)
            self.d.click_opt(sub_xpath)
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
        # for i in range(50):
        #     time.sleep(1)
        #     print i
        # 判断是否登录成功，如果成功则保存cookies
        if self.d.is_element_exist('//input[@id="continue"]'):
            L.error('<login> 登录失败, 要验证码或邮箱验证')
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录失败, 要验证码或邮箱验证')
            if self.check_mail_auth():
                auth = self.get_auth()
                if auth:
                    if self.input_auth(auth):
                        bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '邮箱验证登录成功')
                        return True
                    else:
                        L.error('邮箱验证码提交失败')
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '邮箱验证码提交失败')
                        return False
                else:
                    L.error('未从邮箱获取到验证码')
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '未从邮箱提取到验证码')
                    return False
            else:
                L.error('需要手动验证码或者账号可能被封，请检查')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '需要手动验证码或者账号可能被封，请检查')
                return False
        else:
            bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '账号登录')
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '账号登录', '登录成功')
            return True

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

    def check_mail_auth(self):
        h1_xp = '//h1[contains(text(), "Verification needed")]'
        if self.d.get_elem_counts(h1_xp) > 0:
            return True
        return False

    def send_auth_to_mail(self):
        send_xp = '//input[@id="continue"]'
        self.d.click_opt(send_xp)

    def get_auth(self):
        mail_handler = MailServer(self.conf.user, self.conf.pw,
                                  self.conf.host, self.conf.port)
        if mail_handler.conn:
            origin_len = mail_handler.email_counts()
            L.debug('origin_len:' + origin_len)
            mail_handler.close_server()
            self.send_auth_to_mail()
            for i in range(self.conf.wait_mail):
                L.info('剩余时间:%s(s)' % ((self.conf.wait_mail-i)*10))
                time.sleep(10)

                mail_handler = MailServer(self.conf.user, self.conf.pw,
                                          self.conf.host, self.conf.port)
                if mail_handler.conn:
                    cur_len = mail_handler.email_counts()
                    if cur_len - origin_len > 0:
                        con = mail_handler.parse_mail(cur_len)
                        authcode = mail_handler.abstract_authcode(con)
                        mail_handler.close_server()
                        if authcode:
                            L.debug('auth code:' + authcode)
                            return authcode
                        else:
                            L.error('验证码提取失败')
                    else:
                        L.error('还没获取到新邮件')
                else:
                    L.error('邮箱第%s次链接失败' % (i+1))
        else:
            L.error('邮箱链接失败')

    def input_auth(self, auth):
        h1_xp = '''//h1[contains(text(), "Verifying it's you")]'''
        ctn_xp = '//input[@aria-labelledby="a-autoid-0-announce"]'
        code_xp = '//input[@name="code"]'
        if self.d.get_elem_counts(h1_xp) > 0:
            self.d.send_key(code_xp, auth)
            self.d.click_opt(ctn_xp)
            return True
        return False


if __name__ == '__main__':

    pass

