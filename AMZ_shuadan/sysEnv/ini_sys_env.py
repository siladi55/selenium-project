#coding=utf-8
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
from setSysTimeLang import setSysTime, setScreenPx
from changeMAC.changeMac import set_mac
from db.SQLModel import HandleDB
from logs.log import Logger
L = Logger(__file__)
DB = HandleDB()

def manufacture_mac():
    """随机获取mac厂商标识"""
    sql = "select top(1) * from inventory_mac_manufacture order by newid()"
    return DB.search(sql)[0][1].encode('utf-8')

def setMac(account_guid, mac=None, usage='login'):
    """mofidy the mac for AMZ acoount"""
    assert usage in ["login", 'regist'], 'Please make sure the usage for setMac'
    if usage == 'regist':
        print 'regist mac'
        ind = manufacture_mac()
        # print ind
        res = set_mac(index=ind)
        print 'regist', res
        if res[1]:
            sql = "exec sys_UpdateSysInfo '%s','%s'" % (account_guid, res[0])
            DB.callProc(sql)
        else:
            L.error('新mac：%s 地址连网失败' % res[0])
    elif usage == 'login':
        print 'login mac:', mac
        # table, fields, where = 'sys_ini_env', ['mac'], "Mailbox_G='%s'" % account_guid
        # mac = DB.search_(table, fields, where)
        # if len(mac):
        res = set_mac(mac)
        print res
        # else:
        #     L.error('没找到此账号对应的mac地址，请检查账号')


def ini_sys(sys_conf, usage='login'):
    setMac(sys_conf.guid, sys_conf.mac, usage)
    setSysTime(sys_conf.cid)
    screen = sys_conf.screen_px.split("*")
    setScreenPx(*screen)

if __name__ == '__main__':
    setMac('6BE3BF25-95D4-4BA9-94B9-326C1AFD6F2E', 'login')
