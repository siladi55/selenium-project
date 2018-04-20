#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import hashlib
import GAkw, addTime
from db import SQLModel, info_to_db
from threading import Thread
from Queue import Queue
from log.log import Logger
L = Logger('api.task')



class AddTimeThread(Thread):
    """多线程爬取addTime, 将产品asinMD5放入队列"""
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q

    def run(self):
        while True:
            try:
                asinMD5 = self.q.get(False)
            except:
                break
            else:
                try:
                    ssql = "select ASIN from dbo.产品库 where asinMD5 = '%s'" % asinMD5
                    helper = SQLModel.SQLhelper()
                    res = helper.search(ssql)
                    if len(res):
                        asin = res[0][0]
                        obj = addTime.CrawlAddTime(asin)
                        atime = obj.add_time()
                        info_to_db.addTime_to_db(asinMD5, atime)
                    else:
                        L.debug('No such goods in db')
                except Exception, e:
                    L.exc(e)


def addTime_ctrler(asinMD5List):
    if len(asinMD5List):
        try:
            q = Queue()
            for i in asinMD5List:
                q.put(i)
            threadList = []
            for i in range(3):
                li = AddTimeThread(q)
                threadList.append(li)
            for thread in threadList:
                thread.start()
            for thread in threadList:
                thread.join()
            return 'OK'
        except:
            return -1
    return -1


def adwords(kw, cid):
    kwDict = GAkw.main(kw, cid)
    if kwDict:
        L.debug(kwDict)
        m = hashlib.md5()
        w = 'GA' + str(cid) + kw
        m.update(w)
        GAmd5 = m.hexdigest()
        info_to_db.GAkw_to_db(kwDict, GAmd5)
        return json.dumps(kwDict, ensure_ascii=False)
    else:
        return -1


if __name__ == '__main__':
    # adwords('personal alarm', 1)
    addTime_ctrler(['48893cba197f0ec1b65daa3a7d5e33aa', '99a1dc17372315a90f32417675989c6f','e79134bebe9e76e03f20078fc259cf26'])