#coding=utf-8
from logs.log import Logger
from bs_operations import Driver
from db.SQLModel import Record2DB
L = Logger(__name__)
Rdb = Record2DB()

def update_cookie_to_db(driver, guid, user, task, task_name=''):
    cookies = driver.get_cookies_from_bs()
    if len(cookies):
        if Rdb.update_cookie(user, cookies):
            L.info('入库Cookie 更新成功')
            if len(task_name):
                Rdb.insert_log(guid, user, task, task_name + ': 入库Cookie 更新成功')
            else:
                Rdb.insert_log(guid, user, task, '入库Cookie 更新成功')
        else:
            L.info('入库Cookie 更新失败')
            if len(task_name):
                Rdb.insert_log(guid, user, task, task_name + ': 入库Cookie 更新失败')
            else:
                Rdb.insert_log(guid, user, task, '入库Cookie 更新失败')
    else:
        L.info('入库Cookie 更新失败, 因为没有从浏览器获取到cookie')
        if len(task_name):
            Rdb.insert_log(guid, user, task, task_name + ': 入库Cookie 更新失败，未从浏览器获取到cookie')
        else:
            Rdb.insert_log(guid, user, task, '入库Cookie 更新失败，未从浏览器获取到cookie')

def insert_cookie_to_db(driver, guid, user):
    cookies = driver.get_cookies_from_bs()
    if len(cookies):
        if Rdb.insert_cookie(user, cookies):
            L.info('入库Cookie  新增成功')
            Rdb.insert_log(guid, user, '邮箱注册', '入库Cookie 新增成功')
        else:
            L.info('入库Cookie 新增失败')
            Rdb.insert_log(guid, user, '邮箱注册', '入库Cookie 新增失败')
    else:
        L.info('入库Cookie 新增失败, 因为没有从浏览器获取到cookie')
        Rdb.insert_log(guid, user, '邮箱注册', '入库Cookie 新增失败，未从浏览器获取到cookie')
