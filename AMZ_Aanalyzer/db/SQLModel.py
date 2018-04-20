#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymssql
import chardet
from log.log import Logger
L = Logger("task.DB")


class SQLhelper(object):
    def __init__(self, host='192.168.0.231', user='sa', password='Sa123456', database='test111'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def open(self):
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cur = self.conn.cursor()

    def run(self, sql):
        self.open()
        self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def search(self, sql):
        self.open()
        self.cur.execute(sql)
        res = self.cur.fetchall()
        self.close()
        return res

    def close(self):
        self.cur.close()
        self.conn.close()

# 对查询到的数据进行增删改
def updateExist(ssql, *args): # 如果查询到某结果执行增删改
    helper = SQLhelper()
    res = helper.search(ssql)
    if res[0][0] > 0:
        for i in args:
            helper.run(i)
        L.debug('db有该产品：%s' % ssql)
    else:
        L.debug('db无该产品：%s' % ssql)


def three_month_date():
    sql = 'select convert(nvarchar(10),getdate()-91,120)'  # 获取之前91天的日期
    try:
        helper = SQLhelper()
        date = helper.search(sql)
        return date[0][0]
    except Exception, e:
        L.error(e)


if __name__ == '__main__':
    helper = SQLhelper()
    # sql = "insert into 搜索量(关键词) values ('日替わりタイムセールや、お得なクーポン情報が満載')"
    # res = helper.search(sql)
    # print res
    # sql = "delete from 类目表"
    # helper.run(sql)
    sql = "select 排名 from dbo.产品库 where asinMD5 = 'ceb021d798871a97df6e6429e2782196'"
    res = helper.search(sql)
    print chardet.detect(bytes(res[0][0]))
    print res[0][0]
    # print three_month_date()