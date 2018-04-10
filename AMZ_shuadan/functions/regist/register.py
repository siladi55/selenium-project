#coding=utf-8
import sys
import re
import browser as bo
import setting
import util
from db.SQLModel import Record2DB
from logs.log import Logger
L = Logger(__file__)
Rdb = Record2DB()


class Regist(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf

    def start(self):
        try:
            login_xp = str()
            if self.conf.cid in (2, 5):
                login_xp = '//a[@id="nav-link-yourAccount"]'
            elif self.conf.cid in (1, 3, 4, 6, 7, 8):
                login_xp = '//a[@id="nav-link-accountList"]'
            create_xp = '//a[@id="createAccountSubmit"]'
            yourname = '//input[@id="ap_customer_name"]'
            email_xp = '//input[@id="ap_email"]'
            pw_xp = '//input[@id="ap_password"]'
            recheck_xp = '//input[@id="ap_password_check"]'
            alert = r".*Email address already in use.*"
            ctn_xp = '//input[@id="continue"]'
            url = 'https://' + util.CidTransfer(self.conf.cid).value
            if self.d.request(url):
                if self.d.wait_clickable(login_xp):
                    # self.d.rand_move()
                    self.d.click_opt(login_xp)
                    self.d.wait_clickable(create_xp)
                    self.d.click_opt(create_xp)
                    self.d.wait(yourname)
                    self.d.wait(email_xp)
                    self.d.wait(pw_xp)
                    self.d.wait(recheck_xp)
                    self.d.wait_clickable(ctn_xp)
                    self.d.send_key(yourname, self.conf.yourname)
                    self.d.send_key(email_xp, self.conf.user)
                    self.d.send_key(pw_xp, self.conf.pw)
                    self.d.send_key(recheck_xp, self.conf.pw)
                    self.d.click_opt(ctn_xp)
                    util.rand_stay(5, 8)
                    if re.match(alert, str(self.d.page_source), re.S):
                        # print self.d.is_elements_exist(alert_xp), 'cunzai'
                        L.error('The email has been registed!')
                        Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册失败, 邮箱被注册过')
                        Rdb.callProc("exec sys_InsertAccount '%s',3,'邮箱已注册'" % self.conf.guid)
                        util.rand_stay(5, 6)
                        self.d.quit_opt()
                        return False
                    else:
                        # if self.d.flag:
                        bo.insert_cookie_to_db(self.d, self.conf.guid, self.conf.user)
                        L.info('%s 注册成功' % self.conf.user)
                        Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册成功(个人资料未初始化)')
                        Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功'" % self.conf.guid)
                        return True
                        # else:
                        #     L.info('%s 注册失败' % self.conf.user)
                        #     Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册失败(请检查操作节点)')
                        #     Rdb.callProc("exec sys_InsertAccount '%s',3,'注册失败'" % self.conf.guid)
                        #     self.d.quit_opt()
                        #     return False
                else:
                    L.info('%s 注册失败' % self.conf.user)
                    Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册失败(当前user-agent请求的页面未找到登录节点)')
                    Rdb.callProc("exec sys_InsertAccount '%s',3,'注册失败'" % self.conf.guid)
                    return False
            else:
                L.info('%s 注册失败' % self.conf.user)
                Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册失败(代理网速过慢，请求失败)')
                Rdb.callProc("exec sys_InsertAccount '%s',3,'注册失败'" % self.conf.guid)
                return False
        except Exception, e:
            L.exc('<regist>: 注册失败。(%s)' % e)
            Rdb.insert_log(self.conf.guid, self.conf.user, '邮箱注册', '注册失败(请检查操作节点)')
            Rdb.callProc("exec sys_InsertAccount '%s',3,'注册失败'" % self.conf.guid)
            return False


if __name__ == '__main__':
    conf = setting.ChromeConf()  # 可传入浏览器参数类，修改设置参数
    driver = bo.Initial_browser(conf).set_chrome()  # 初始化浏览器
    d = bo.Driver(driver)
    Regist(d, 1, setting.CONF['yourname'], setting.CONF['user'], setting.CONF['pw']).start()