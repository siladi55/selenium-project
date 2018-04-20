# coding=utf-8
import functions as func
import db.get_params_from_db as g
import browser as  bo
from sysEnv.ini_sys_env import ini_sys
from logs.log import Logger
from setting import *
from db.SQLModel import Record2DB
Log = Logger(__file__)
Rdb = Record2DB()


class Work(object):

    def _regist(self, reg_par):
        reg_conf = RegistConf(reg_par)
        bs_conf = BrowserConf(g.browser_params(reg_conf.guid))
        dr_conf = DriverConf(g.driver_params())
        sys_conf = SysEnvConf(g.env_params(reg_conf.guid))
        ini_sys(sys_conf, 'regist')
        driver = bo.ini_browser_drive(bs_conf, dr_conf)
        if func.Regist(driver, reg_conf).start():
            return True, driver
        else:
            return False, driver

    def _add_addr(self, driver, reg_params):
        addr = g.addr_params(reg_params)
        if len(addr) > 2:
            ad_conf = AddrConf(addr)
            func.addAddr.add_address(driver, ad_conf)
        else:
            Rdb.insert_log(reg_params['task_guid'], reg_params['user'], '邮箱注册', '注册成功，地址添加失败(没获取到地址参数)')

    def _add_head_img(self, driver, reg_params):
        pro_params = g.profile_params(reg_params)
        if len(pro_params) > 2:
            pf_conf = ProfileConf(pro_params)
            func.head_img.add_profile(driver, pf_conf)
        else:
            Rdb.insert_log(reg_params['task_guid'], reg_params['user'], '邮箱注册', '注册成功，画像失败(没获取到画像参数),初始化失败')


    def regist_ini_account(self, guid):
        par = g.regist_params(guid)
        print 'par', par
        if len(par):
            flag, driver = self._regist(par)
            if flag:
                if par['typeId'] == 1:
                    self._add_addr(driver, par)
                    self._add_head_img(driver, par)
            driver.quit_opt()

    def _login_initial(self, guid):
        g.distribute_account(guid)  # 账号分配
        bs_conf = BrowserConf(g.browser_params(guid, 'login'))
        dr_conf = DriverConf(g.driver_params())
        sys_conf = SysEnvConf(g.env_params(guid, 'login'))
        par = g.login_params(guid)
        if len(par):
            lg_conf = LoginConf(par)
            ini_sys(sys_conf, 'login')
            driver = bo.ini_browser_drive(bs_conf, dr_conf)
            if lg_conf.by_click:  # 手动登录
                if func.Login(driver, lg_conf).login_by_click():
                    return driver
                else:
                    Log.error('<login initial>: 点击登录失败')
            else:  # cookie登录
                if func.Login(driver, lg_conf).login_with_cookie():
                    return driver
                else:
                    Log.error('<login initial>: 带cookie登录失败')
        else:
            Log.error('<login initial>: 账号未分配')

    def search_initial(self, guid):
        driver = self._login_initial(guid)
        if driver is not None:
            par = g.search_params(guid)
            print 'searchpar', par
            if len(par):
                sc_conf = SearchConf(par)
                if func.InnerTraffic(driver, sc_conf).search():
                    return driver
                else:
                    Log.error('<search initial>: Not found product')
            else:
                Log.error('<search initial>: Failed to aquire search params')

    def manual_opt_after_login(self, guid, minute):
        par = g.manual_login_params(guid)
        if len(par):
            bs_conf = BrowserConf(par)
            dr_conf = DriverConf(g.driver_params())
            sys_conf = SysEnvConf(par)
            lg_conf = LoginConf(par)
            ini_sys(sys_conf, 'login')
            driver = bo.ini_browser_drive(bs_conf, dr_conf)
            if func.Login(driver, lg_conf).login_with_cookie():
                Log.info('<manual operation>: 带cookie登录成功')
                for i in range(1, minute * 60):
                    time.sleep(1)
                    print '%s后浏览器关闭，请勿手动关闭浏览器' % (60 * minute - i)
                # print '更新cookie'
                bo.update_cookie_to_db(driver, guid, lg_conf.user, '账号?登录')
                print '操作成功'
            else:
                Log.error('<manual operation>: 带cookie登录失败')
        else:
            Log.error('<manual operation>: 手动登录未获取到参数')

    def _add2cart(self, driver, conf):
        return func.Actions(driver, conf).add_to_cart()

    def _add2list(self, driver, conf):
        return func.Actions(driver, conf).add_to_list()

    def _qa_vote(self,driver, conf):
        return func.QA(driver, conf).vote_opt()

    def _qa_yes_no(self,driver, conf):
        return func.QA(driver, conf).yes_no_opt()

    def _review_yes_no(self, driver, conf):
        return func.Review(driver, conf).yes_no_opt()

    def _shopping(self, driver, task_guid):
        try:
            sp_conf = ShoppingConf(g.shopping_params(task_guid))
            return func.Shopping(driver, sp_conf).proceed_checkout()
        except:
            Log.error('<shopping>: 购买失败')
            return False

    def traffic_task(self, task_guid):
        driver = self.search_initial(task_guid)
        if driver is not None:
            par = g.task_params(task_guid)  # 获取任务id
            if len(par):
                task_conf = TaskGuid(par)
                if task_conf.task_id == 6:
                    if self._add2cart(driver, task_conf):
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '添加购物车成功', 1" % task_guid)
                    else:
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '添加购物车失败', 2" % task_guid)
                elif task_conf.task_id == 5:
                    if self._add2list(driver, task_conf):
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '添加收藏成功', 1" % task_guid)
                    else:
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '添加收藏失败', 2" % task_guid)
                elif task_conf.task_id == 3:
                    try:
                        rv_params = g.traffic_params(task_guid, 1)
                        rev_conf = TrafficActConf(rv_params)
                        if self._review_yes_no(driver, rev_conf):
                            Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '评论helpful成功', 1" % task_guid)
                        else:
                            Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '评论helpful失败', 2" % task_guid)
                    except:
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '评论helpful失败', 2" % task_guid)
                elif task_conf.task_id == 10:
                    try:
                        qa_params = g.traffic_params(task_guid, 2)
                        qa_conf = TrafficActConf(qa_params)
                        if qa_conf.answerer_id is not None:
                            if self._qa_yes_no(driver, qa_conf):
                                Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '问答QA成功', 1" % task_guid)
                            else:
                                Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '问答QA失败', 2" % task_guid)
                        else:
                            if self._qa_vote(driver, qa_conf):
                                Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '问答QA成功', 1" % task_guid)
                            else:
                                Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '问答QA失败', 2" % task_guid)
                    except:
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '问答QA失败', 2" % task_guid)
                elif task_conf.task_id == 7:
                    if self._shopping(driver, task_guid):
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '购买成功', 1" % task_guid)
                    else:
                        Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '购买失败', 2" % task_guid)
            else:
                Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '任务id获取失败', 2" % task_guid)
            # the next line blocked for testing, browser should be active
            driver.quit_opt()
        else:
            Rdb.callProc("exec sys_UpdateTaskStatus  '%s', '任务初始化失败', 2" % task_guid)
            Log.error('任务失败')


if __name__ == '__main__':
    # bs_conf = BrowserConf()
    # dr_conf = DriverConf()
    # sys_conf = SysEnvConf()
    # lg_conf = LoginConf()
    # ini_sys(sys_conf, 'login')
    # driver = bo.ini_browser_drive(bs_conf, dr_conf)
    # print 'driver chushihua '
    # l = func.Login(driver, LoginConf()).login_with_cookie()
    # print 'finished'
    # while 1:
    #     pass
    Work().traffic_task('')






