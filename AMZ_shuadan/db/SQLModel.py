#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymssql
from logs.log import Logger
L = Logger(__name__)


class SQLhelper(object):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def open(self):
        try:
            self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            self.cur = self.conn.cursor()
        except Exception, e:
            L.exc('数据库连接失败：%s' % e)

    def run(self, sql):
        try:
            self.open()
            self.cur.execute(sql)
            self.conn.commit()
            self.close()
            return 1
        except Exception, e:
            L.exc('执行错误(%s): %s' % (sql, e))
            return 0

    def search(self, sql):
        try:
            self.open()
            self.cur.execute(sql)
            res = self.cur.fetchall()
            self.close()
            return res
        except Exception, e:
            L.exc("查询错误(%s): %s" % (sql, e))
            return []

    def callProc(self, sql):
        try:
            self.open()
            self.cur.execute(sql)
            res = self.cur.fetchall()
            self.conn.commit()
            self.close()
            return res
        except Exception, e:
            L.exc(" 存储过程错误(%s): %s" % (sql, e))
            return []

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception, e:
            L.exc('断开DB错误：%s' % e)

class HandleDB(SQLhelper):
    def __init__(self, host='192.168.0.231', user='sa', password='Sa123456', database='vp'):
        super(HandleDB, self).__init__(host, user, password, database)

    def insert_(self, table, fields, values):
        if not (isinstance(fields, list) and isinstance(values, list) and len(fields) == len(values)):
            raise ValueError('Params field and values should be type list with the same length')
        try:
            # sql = 'insert into {0} ({1}) values ({2})'.format(table, fields, values)
            sql = 'insert into %s (' % table
            for i in fields:
                sql += i+', '
            sql = sql[:-2] + ') values ('
            for i in values:
                sql += "'" + i.replace("'", "&acute;") + "', "
            sql = sql[:-2] + ')'
            sql = sql.replace("'getdate()'", "getdate()").replace('"getdate()"', "getdate()")
            # print sql
            return self.run(sql)
        except Exception, e:
            L.exc('<insert>:%s'%e)
            return 0

    def update_(self, table, fields, values, where):
        if not (isinstance(fields, list) and isinstance(values, list) and len(fields) == len(values)):
            raise ValueError('Params field and values should be type list with the same length')
        try:
            # sql = 'update {0} set {1}={2} where {3}'.format(table, fields, values, where)
            sql = 'update %s set ' % table
            new_tuple = zip(fields, values)
            for i in new_tuple:
                sql += "%s = '%s', " % (i[0], i[1].replace("'", "&acute;"))
            sql = sql[:-2] + ' where ' + where
            # print sql
            sql = sql.replace("'getdate()'", "getdate()").replace('"getdate()"', "getdate()")
            return self.run(sql)
        except Exception, e:
            L.exc('<update>:%s'%e)
            return 0

    def search_(self, table, fields, where=''):
        assert isinstance(where, str), \
            '\'where\' expression should be type<string>, but got %s' % type(where)
        assert isinstance(fields, list), 'Params fields should be type<list>.'
        try:
            sql = 'select '
            for i in fields:
                sql += i + ', '
            sql = sql[:-2] + ' from ' + table
            if len(where):
                sql += ' where ' + where
                # print sql
            # print sql
            return self.search(sql)
        except Exception, e:
            L.exc(e)
            return []

    def delete_(self, table, where):
        try:
            sql = 'delete from {0} where {1}'.format(table, where)
            # print sql
            return self.run(sql)
        except Exception, e:
            L.exc('<delete>:%s'%e)
            return 0

class Record2DB(HandleDB):
    def __init__(self, host='192.168.0.100', user='sa', password='Sa123456', database='vp'):
        super(Record2DB, self).__init__(host, user, password, database)

    def insert_to_db(self, fields, values, table):
        """Record execution logs to db"""
        return self.insert_(table, fields, values)

    def update_to_db(self, field, value, where, table):
        """Update the execution logs"""
        return self.update_(table, field, value, where)

    def insert_log(self, *val):
        table = 'sys_execution_logs'
        fields = ['task_G', 'amazon_login_account', 'task_type', 'log_content', 'last_update']
        values = [i for i in val]
        values.append('getdate()')
        return self.insert_(table, fields, values)

    def sum_trackno(self, task_guid, val_sum, val_order):
        table = 'sys_Task_List_Detailed'
        fields = ['TotalAmount', 'OrderNumber']
        values = [val_sum, val_order]
        where = "Task_List_G='%s'" % task_guid
        return self.update_to_db(fields, values, where, table)

    def gift_card_balance(self, task_guid, bal):
        table, field, value, where = 'sys_Task_List_Detailed', ['Amountbalance'], [bal], "Task_List_G='%s'" % task_guid
        return self.update_to_db(field, value, where, table)

    def update_cookie(self, user, ck):
        table, fields, values, where = 'account_cookies', ['cookies'], [ck], "account='%s'" % user
        return self.update_(table, fields, values, where)

    def insert_cookie(self, user, ck):
        table, fields, values = 'account_cookies', ['account', 'cookies'], [user, ck]
        return self.insert_(table, fields, values)


if __name__ == '__main__':
    h = HandleDB()
    # h.search_(table="tablex", fields=['a','b','c'], where='condition expression')
    # h = Record2DB()
    # h.insert_log('user', 'task', 'log')
    # res = h.callProc("exec sys_SelectMailboxList")
    # print res
    # print res[0][1]
    import csv
    con = h.search('select useragent, useragent_platform, operation_system, browser_version from sys_User_agent_inventroy')
    with open("test.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["user_agent", "platform", 'os', 'browser_version'])
        # 写入多行用writerows
        writer.writerows([[a,b,c,d] for a,b,c,d in con])
