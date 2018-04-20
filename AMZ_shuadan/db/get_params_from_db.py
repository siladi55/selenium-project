#coding=utf-8
from db import SQLModel
from logs.log import Logger
L = Logger(__file__)
DB = SQLModel.HandleDB()


def env_params(guid, usage='regist'):
    assert usage in ["login", 'regist'], 'Please make sure the usage for params'
    par = {}
    if usage == 'regist':
        sql = "exec sys_CreateSysInfo '%s'" % guid
        params = DB.callProc(sql)
        print 'env_param', params
    else:
        sql = "exec sys_GetAccountParameter '%s', 1" % guid  # task_guid
        params = DB.callProc(sql)
        print 'env_param', params
    if len(params[0]) > 1:
        if params[0][1]: par['guid'] = str(params[0][1])
        if params[0][2]: par['mac'] = params[0][2]
        if params[0][3]: par['sys_lang'] = params[0][3]
        if params[0][4]: par['screen_px'] = params[0][4]
        if params[0][5]: par['cid'] = params[0][5]
    return par


def browser_params(guid, usage='regist'):
    assert usage in ["login", 'regist'], 'Please make sure the usage for params'
    par = {}
    if usage == 'regist':
        sql = "sys_CreateBrowserInfo '%s'" % guid
        params = DB.callProc(sql)
        print 'browser_params1', params
    else:
        sql = "exec sys_GetAccountParameter '%s', 2" % guid  # task_guid
        params = DB.callProc(sql)
        print 'browser_params2', params
    if len(params):
        if len(params[0]) > 1:
            if params[0][1]:
                par['guid'] = str(params[0][1])
            if params[0][2]:
                par['user_agent'] = params[0][2]
            if params[0][3]:
                par['font'] = params[0][3]
            if params[0][4]:
                par['acpt_lang'] = params[0][4]
            if params[0][5]:
                par['proxy'] = params[0][5]
    else:
        L.error('存储过程：%s 返回数据为空' % sql)
    return par

def driver_params():
    par = {}
    table, fields, where = 'sys_Configuration', \
                           ['stay_time', 'waitime', 'page_offset', 'page_move_rate', 'rand_move_lenth'], 'id=1'
    params = DB.search_(table, fields, where)
    print 'driver params', params
    if len(params):
        st = params[0][0].split('*')
        pmr = params[0][3].split('*')
        rml = params[0][4].split('*')
        par['stay_time'] = (int(st[0]), int(st[1]))
        par['waitime'] = int(params[0][1])
        par['page_offset'] = int(params[0][2])
        par['page_move_rate'] = (int(pmr[0]), int(pmr[1]))
        par['rand_move_lenth'] = (int(rml[0]), int(rml[1]))
    return par

def regist_params(guid):
    par = {}
    para_list = DB.callProc("exec sys_SelectMailboxList '%s'" % guid)
    print 'regist_params', para_list
    if len(para_list[0]) > 1:
        par['guid'] = str(para_list[0][1])
        par['yourname'] = para_list[0][4]
        par['user'] = para_list[0][2]
        par['pw'] = para_list[0][3]
        par['cid'] = para_list[0][5]
        par['typeId'] = para_list[0][6]
    return par


def addr_params(params, usage='regist'):
    assert usage in ["deliver", 'regist'], 'Please make sure the usage for params'
    par = {}
    if usage == 'regist':
        assert params.has_key('guid')
        assert params.has_key('user')
        par = {'user': params['user'], 'guid': str(params['guid'])}
        sql = "exec sys_getAddressInfo '%s'" % params['guid']
        para_list = DB.callProc(sql)
    else:
        sql = "exec sys_GetDistributionInfo '%s', 1" % params  # 传入address guid
        para_list = DB.callProc(sql)
    print 'addr_params', para_list
    if len(para_list[0]) > 1:
        if para_list[0][1]: par['addr_guid'] = str(para_list[0][1])
        # if para_list[0][2]: par['guid'] = para_list[0][2]
        if para_list[0][3]: par['addr_cty'] = para_list[0][3]
        if para_list[0][4]: par["fullname"] = para_list[0][4]
        if para_list[0][5]: par['state'] = para_list[0][5]
        if para_list[0][6]: par['city'] = para_list[0][6]
        if para_list[0][7]:
            par['streetaddr'] = para_list[0][7]
        elif para_list[0][8]:
            par['streetaddr'] = para_list[0][8]
        if para_list[0][9]: par['zip_code'] = para_list[0][9]
        if para_list[0][10]: par['phoneNo'] = para_list[0][10]
    return par

def profile_params(reg_params):
    assert reg_params.has_key('guid')
    assert reg_params.has_key('user')
    par = {'user': reg_params['user'], 'guid': str(reg_params['guid'])}
    sql = "exec sys_getProfilesInfo '%s'" % reg_params['guid']
    para_list = DB.callProc(sql)
    print 'profile_param', para_list
    if len(para_list[0]) > 1:
        if para_list[0][1]: par['profile_guid'] = str(para_list[0][1])
        if para_list[0][3]: par['bio'] = para_list[0][3]
        if para_list[0][4]: par['occupation'] = para_list[0][4]
        if para_list[0][5]: par['website'] = para_list[0][5]
        if para_list[0][6]: par['location'] = para_list[0][6]
        if para_list[0][7]: par['email_addr'] = para_list[0][7]
        if para_list[0][8]: par['fb'] = para_list[0][8]
        if para_list[0][9]: par['pint'] = para_list[0][9]
        if para_list[0][10]: par['twitter'] = para_list[0][10]
        if para_list[0][11]: par['instagram'] = para_list[0][11]
        if para_list[0][12]: par['youtube'] = para_list[0][12]
        if para_list[0][13]: par['imgPath'] = para_list[0][13]
    print 'par', par
    return par


def login_params(guid):
    par = {}
    sql = "exec sys_GetAccountParameter '%s', 3" % guid  # task_guid
    params = DB.callProc(sql)
    print 'login_params', params
    if len(params[0]) > 1:
        if params[0][5]:
            par['user'] = params[0][5].encode('utf-8')
        if params[0][6]:
            par['pw'] = params[0][6]
        if params[0][7]:
            par['cid'] = params[0][7]
        if params[0][12]:
            par['name'] = params[0][12]
        par['task_guid'] = str(guid)
    return par


def distribute_account(guid):
    """just execute this function for SQL SERVER to distribute an account for a task
        It makes no sense to current package
    """
    sql = "exec sys_GetAccountParameter '%s', 0" % guid  # task_guid
    DB.callProc(sql)

def search_params(guid):
    par = {}
    sql = "exec sys_GetAccountParameter '%s', 4" % guid  # task_guid
    params = DB.callProc(sql)
    print 'search_params', params
    if len(params[0]) > 1:
        if params[0][0]: par['cid'] = params[0][0]
        if params[0][1]: par['asin'] = params[0][1]
        if params[0][2]: par['kw'] = params[0][2]
        if params[0][3]: par['option_value'] = params[0][3]
        if params[0][4]: par['cata'] = params[0][4]
        if params[0][5]: par['search_price'] = (params[0][5], params[0][5]+5)
        if params[0][6]: par['search_page'] = params[0][6]
        par['ignore_sponsored'] = 0 if params[0][7] else 1
        if params[0][8]: par['user'] = params[0][8]
        par['task_guid'] = str(guid)
    return par


def traffic_params(task_guid, usage=1):
    """usage: 1-->review, 2-->QA"""
    assert usage in (1, 2), 'Wrong params "usage" for tracffic_params'
    par = {}
    sql = "exec sys_SelectTaskDetailed '%s', %s" % (task_guid, usage)
    params = DB.callProc(sql)
    print 'traffic_params', params
    if len(params[0]) > 1:
        if usage == 1:
            if params[0][0]: par['review_title'] = params[0][0]
            if params[0][1]: par['review_author'] = params[0][1]
            if params[0][2] is not None: par['review_help'] = params[0][2]
            if params[0][3]: par['user'] = params[0][3]
        elif usage == 2:
            if params[0][0]: par['question_id'] = params[0][0]
            if params[0][1]:
                par['answerer_id'] = params[0][1]
                if params[0][2] is not None: par['answer_help'] = params[0][2]
            else:
                if params[0][2] is not None: par['vote'] = params[0][2]
            if params[0][3]: par['user'] = params[0][3]
        par['task_guid'] = str(task_guid)
    return par

def shopping_params(taskguid):
    par = {}
    sql = "exec sys_SelectTaskDetailed '%s', 3" % taskguid
    params = DB.callProc(sql)
    print 'shop params', params
    if len(params[0]) > 1:
        if params[0][0]: par['user'] = params[0][0]
        if params[0][1] is not None: par['buy_cart'] = params[0][1]
        if params[0][2]: par['shop_name'] = params[0][2]
        if params[0][3]: par['shop_id'] = params[0][3]
        if params[0][4] is not None: par['fba'] = params[0][4]
        if params[0][5]: par['newAddrGuid'] = params[0][5]
        if params[0][6]: par['ccard_guid'] = params[0][6]
        if params[0][7]: par['giftcard_guid'] = params[0][7]
        par['task_guid'] = str(taskguid)
    print 'shopppar', par
    sql = "exec sys_GetAccountParameter '%s', 3" % taskguid  # task_guid
    params = DB.callProc(sql)
    print 'ship_login_params', params
    if len(params[0]) > 1:
        if params[0][6]: par['pw'] = params[0][6]
        if params[0][7]: par['cid'] = params[0][7]
    return par

def card_params(ccname, ccard_guid=None, gift_guid=None):
    par = {}
    if ccard_guid:
        par['ccname'] = ccname
        sql = "exec sys_GetDistributionInfo '%s', 2" % ccard_guid
        params = DB.callProc(sql)
        if len(params[0]) > 1:
            # if params[0][2]: par['ccname'] = params[0][2]
            if params[0][3]: par['ccNo'] = params[0][3]
            if params[0][4]: par['exp_mon'] = params[0][4]
            if params[0][5]: par['exp_year'] = params[0][5]
    if gift_guid:
        sql = "exec sys_GetDistributionInfo '%s', 3" % gift_guid
        params = DB.callProc(sql)
        if len(params[0]) > 1:
            if params[0][2]: par['gift_code'] = params[0][2]

    print 'cardInfo:', par
    return par


def task_params(guid):
    par = {}
    sql = "exec sys_SelectTaskList '%s'" % guid  # task guid
    params = DB.callProc(sql)
    print 'task_params', params
    if len(params[0]) > 1:
        if params[0][0]: par['task_guid'] = str(params[0][0])
        if params[0][1]: par['task_id'] = params[0][1]
        if params[0][2]: par['user'] = params[0][2]
    return par

def manual_login_params(guid):
    par = {}
    sys_sql = "exec sys_LoginInfo '%s', 1" % guid
    bs_sql = "exec sys_LoginInfo '%s', 2" % guid
    lg_sql = "exec sys_LoginInfo '%s', 3" % guid
    sys_p = DB.callProc(sys_sql)
    bs_p = DB.callProc(bs_sql)
    lg_p = DB.callProc(lg_sql)
    if len(sys_p) and len(bs_p) and len(lg_p):
        if sys_p[0][2]: par['mac'] = sys_p[0][2]
        if sys_p[0][3]: par['sys_lang'] = sys_p[0][3]
        if sys_p[0][4]: par['screen_px'] = sys_p[0][4]
        if sys_p[0][5]: par['cid'] = sys_p[0][5]

        if bs_p[0][2]: par['user_agent'] = bs_p[0][2]
        if bs_p[0][3]: par['font'] = bs_p[0][3]
        if bs_p[0][4]: par['acpt_lang'] = bs_p[0][4]
        if bs_p[0][5]: par['proxy'] = bs_p[0][5]

        if lg_p[0][5]: par['user'] = lg_p[0][5].encode('utf-8')
        if lg_p[0][6]: par['pw'] = lg_p[0][6]
        if lg_p[0][12]: par['name'] = lg_p[0][12]
    return par



if __name__ == '__main__':
    # print addr_params('61A19F3C-B960-450C-975D-2097BCC3210C')
    # sys_env_params('3215063@qq.com')
    sql = "exec sys_UpdateTaskStatus 'D5ECB708-912D-4DE6-BD04-12C66B5D3786', '', 2"
    DB.callProc(sql)