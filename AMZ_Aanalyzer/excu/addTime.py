#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import json
import time
import requests
from threading import Thread
from Queue import Queue
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import Basic
from log.log import Logger
L = Logger("task.AddTime")


class Conphantomjs(object):
    phantomjs_max=10           ##同时开启phantomjs个数
    jiange=0.01                  ##开启phantomjs间隔

    def __init__(self):
        self.q_phantomjs = Queue()
        self.resQue = Queue()

    def getbody(self, asinDict):
        driver = self.q_phantomjs.get()
        url = asinDict[asinDict.keys()[0]][-1]
        try:
            driver.get(url)
            driver.refresh()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'priceHistory')))

        except:
            # print '!! Page loaded timeout or not available url:%s' % url
            asinDict[asinDict.keys()[0]].append("None")
            self.resQue.put(asinDict)
        else:
            con = driver.page_source
            page_selector = etree.HTML(con)
            add_time = page_selector.xpath('//div[@id="graph"]//table//tr[last()]/td[2]/table//tr[last()]/td[2]/text()')
            if add_time:
                addTime = add_time[0].split("(")[1].split(" ")[0]
                # print '%s Add time: %s'%(url, addTime)
                asinDict[asinDict.keys()[0]].append(addTime)
                self.resQue.put(asinDict)
            else:
                # print '>> Failed to locate add time node'
                asinDict[asinDict.keys()[0]].append("None")
                self.resQue.put(asinDict)
            # driver.get('http://httpbin.org/ip')
            # print driver.page_source
        self.q_phantomjs.put(driver)


    def open_phantomjs(self):
        '''
        多线程开启phantomjs进程
        '''
        def open_threading():
            chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument('user-agent=' + random.choice(Basic().USER_AGENT))
            # proxy = '--proxy-server=http://' + ip_port
            proxy = '--proxy-server=http://192.168.0.5:26660'
            options.add_argument(proxy)
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
            driver.set_page_load_timeout(60)
            self.q_phantomjs.put(driver)  # 将phantomjs进程存入队列

        th = []
        for i in range(Conphantomjs.phantomjs_max):
            t = Thread(target=open_threading)
            th.append(t)
        for i in th:
            time.sleep(Conphantomjs.jiange)  # 设置开启的时间间隔
            i.start()
        for i in th:
            i.join()

    def close_phantomjs(self):
        '''
        多线程关闭phantomjs对象
        '''
        th = []

        def close_threading():
            driver = self.q_phantomjs.get()
            driver.quit()

        for i in range(self.q_phantomjs.qsize()):
            t = Thread(target=close_threading)
            th.append(t)
        for i in th:
            i.start()
        for i in th:
            i.join()

def main(asinList, m=5):
    """m: the num of phantomjs opened everytime"""
    li = []
    for i in range(len(asinList)):
        asindict = {}
        asindict[i] = [asinList[i], 'https://keepa.com/iframe_addon.html#1-0-' + asinList[i]]
        li.append(asindict)
    print li
    cur = Conphantomjs()
    Conphantomjs.phantomjs_max = m
    cur.open_phantomjs()
    print "phantomjs num is ", cur.q_phantomjs.qsize()
    th = []
    for i in li:
        t = Thread(target=cur.getbody, args=(i,))
        th.append(t)
    for i in th:
        i.start()
    for i in th:
        i.join()
    cur.close_phantomjs()
    print "phantomjs num is ", cur.q_phantomjs.qsize()
    info = list()
    for i in range(cur.resQue.qsize()):
        info.append(cur.resQue.get())

    print json.dumps(info, ensure_ascii=False)
    # k = 0
    # while True:
    #     thr = []
    #     newList = li[k: m+k]
    #     if len(newList):
    #         cur.open_phantomjs()
    #         print "phantomjs num is ", cur.q_phantomjs.qsize()
    #         for i in newList:
    #             t = Thread(target=cur.getbody, args=(i,))
    #             thr.append(t)
    #         for i in thr:
    #             i.start()
    #         for i in thr:
    #             i.join()
    #
    #         cur.close_phantomjs()
    #         print "phantomjs num is ", cur.q_phantomjs.qsize()
    #         k += m
    #     else:
    #         break


if __name__ == '__main__':
    print time.ctime()
    url_list = ['B075CMV89H',
                'B0777C4F1D',
                'B0779PZPDL',
                'B07695TCRF',
                'B0749M2P9Q',
                'B0778G7TCC',
                'B077QPZ1SQ',
                'B077P861V7',
                'B075KP6T43',
                'B0778K83GR',
                'B077D7D9TH',
                'B06XXSGQD2',
                'B075L2W1MR',
                'B0749L8TQF']
    main(url_list, m=3)
    print time.ctime()