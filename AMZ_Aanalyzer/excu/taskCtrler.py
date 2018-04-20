#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import hashlib
import GAkw
from addTime import Conphantomjs
from db import SQLModel, info_to_db
from threading import Thread
from log.log import Logger
L = Logger('api.task')


def addTime_ctrler(asinMD5List, m=10):
    helper = SQLModel.SQLhelper()
    if len(asinMD5List):
        asinList = []
        for asinMD5 in asinMD5List:
            singleDict = {}
            try:
                ssql = "select ASIN from dbo.产品库 where asinMD5 = '%s'" % asinMD5
                res = helper.search(ssql)
                if len(res):
                    url = 'https://keepa.com/iframe_addon.html#1-0-' + res[0][0]
                    singleDict[asinMD5] = [res[0][0], url]
                    asinList.append(singleDict)
                else:
                    singleDict[asinMD5] = ["None", 'None']
            except Exception, e:
                print e
        cur = Conphantomjs()
        Conphantomjs.phantomjs_max = m
        cur.open_phantomjs()
        print "phantomjs num is ", cur.q_phantomjs.qsize()
        th = []
        for i in asinList:
            t = Thread(target=cur.getbody, args=(i,))
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()
        cur.close_phantomjs()
        print "phantomjs num is ", cur.q_phantomjs.qsize()
        info = []
        for i in range(cur.resQue.qsize()):
            item = cur.resQue.get()
            print item
            info.append(item)
        for i in info:
            info_to_db.addTime_to_db(i.keys()[0], i[i.keys()[0]][-1])
        #---------------------------------
        # cur = Conphantomjs()
        # Conphantomjs.phantomjs_max = m
        # k = 0
        # while True:
        #     thr = []
        #     newList = asinList[k: m + k]
        #     if len(newList):
        #         Conphantomjs.phantomjs_max = len(newList)
        #         cur.open_phantomjs()
        #         print "phantomjs num is ", cur.q_phantomjs.qsize()
        #         for i in newList:
        #             t = Thread(target=cur.getbody, args=(i,))
        #             thr.append(t)
        #         for i in thr:
        #             time.sleep(0.5)
        #             i.start()
        #         for i in thr:
        #             i.join()
        #         cur.close_phantomjs()
        #         print "phantomjs num is ", cur.q_phantomjs.qsize()
        #         info = []
        #         for i in range(cur.resQue.qsize()):
        #             item = cur.resQue.get()
        #             info.append(item)
        #         for i in info:
        #             info_to_db.addTime_to_db(i.keys()[0], i[i.keys()[0]][-1])
        #         print json.dumps(info, ensure_ascii=False)
        #         k += m
        #     else:
        #         break
    return 'OK'

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

def test():
    print "is it OK?"
    return "is it OK"

if __name__ == '__main__':
    print time.ctime()
    l = ['24968262a35b8620a8b9ccc5ca83c6e5',
         '5b20e6a048d591a7349c89016aa0f7db',
         '6158c01da0a475fdb13fc94ce0034779',
         '864a9c94a823c5e1c0f1847f45712148',
         '83c5f19730f446a308fada3cf58da6c7',
         '8f8b43c5542b7e32fe65d0732531dd68',
         'ac2d90d65bd2fe83d510ccc65db68a22',
         'c1b7cd54d521c38b78e159cfc61e41a6',
         'f07555ec7384ec8a4965c02b4b610214',
         '0d76c286e1b3709b4274bc9fe0bde24e',
         '6e8a087ebc5478e06e72f6091743278c',
         'a5dbe1d7ccb53c56b52081ff96c89f1a',
         '317d86a794d3507f834b6ca7bad7a314',
         'f3a65a0d01b4f829e01a77066ffa3fb9',
         'b5a7284abb88fe7622aad538e92a6097',
         'c218ed76eeeb8494c72fdd2fe3285665',
         '2d20e89ee71e0b5dd70d906c695743fe',
         'c2d0bf24ef5ba0becb5d9fa69b29c1c2',
         'bfcba197d46bd7eca3e7f5e422ffd068',
         '96815438ce7146ff7e09454ebe647fb4',
         'f8b6a6d801884ccaba1153be4ee666f3',
         '9ac543ff177a1900e475239acb69ce10',
         '70636803b77ec67813f6033de17c7157',
         '3d4529ee341dab76530033f2336ab081',
         '759445e7c4fdcb8204cc1ab7adec744d',
         '97bb9fa16d9203ad37027edd83abfc33',
         '749965045372efb4462c9535e39cf9cf',
         'df418b46e8e499c7d1554bec58fa21df',
         '0b78d5763fa2cd8492093a31cc4017c4',
         'd838f5846a44a12057f393ebf661d583'
         ]
    addTime_ctrler(l[18:25], m=6)
    print time.ctime()
    # review_ctrler(asinMD5List=['8e48bdbed277e2ceedfb9acda62e788b', 'f3a65a0d01b4f829e01a77066ffa3fb9']) #, 'ac2d90d65bd2fe83d510ccc65db68a22'])
