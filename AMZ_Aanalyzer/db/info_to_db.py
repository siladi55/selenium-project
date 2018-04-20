#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from db import SQLModel
from log.log import Logger
L = Logger("task.info2DB")


def addTime_to_db(asinMD5, aTime):
    """上架时间入库"""
    sql_at = "UPDATE dbo.产品库 SET 上架时间 = '%s' WHERE asinMD5 = '%s'" % (aTime, asinMD5)
    try:
        helper = SQLModel.SQLhelper()
        helper.run(sql_at)
    except Exception as e:
        L.exc("%s 上架时间更新失败 %s" % (asinMD5, e))

def  GAkw_to_db(dataDict, kwMD5):
    helper = SQLModel.SQLhelper()
    ssql = "select count(1) from dbo.keyword表 where MD5s = '%s'" % kwMD5
    sql1 = "DELETE FROM dbo.keyword表 WHERE MD5s = '%s'" % kwMD5
    try:
        SQLModel.updateExist(ssql, sql1)
    except Exception as e:
        L.exc("%s 删除失败%s" % (kwMD5, e))
    for i in range(len(dataDict)):
        sql_GAkw = "insert into dbo.keyword表(keyword, sequence, rank, platform, rankRange, kw组别, countryId, MD5s) values " \
                   "('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            dataDict[i][0].replace("'", "&acute;"), i, dataDict[i][3], 'GA', dataDict[i][2].replace('M', '000000').replace('K', '000'),
            dataDict[0][0], dataDict[i][1], kwMD5)
        try:
            helper.run(sql_GAkw)
        except Exception as e:
            L.exc("No.%s 入库失败 %s" % (i, e))

if __name__ == '__main__':
    pass

