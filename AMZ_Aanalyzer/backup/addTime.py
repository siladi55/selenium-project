#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import Basic
from log.log import Logger
L = Logger("task.AddTime")


class CrawlAddTime(object):
    def __init__(self, asin):
        self.asin = asin
        self.ua = random.choice(Basic().USER_AGENT)

    # ASIN码必须是页面里的默认的ASIN变体的ASIN请求不到keepa数据, zanshibuyong
    def crawl_pageAsin(self, page):
        try:
            selector = etree.HTML(page)
            node = selector.xpath('//div[@id="detail-bullets"]//li[contains(b,"ASIN")]/text()')
            node2 = selector.xpath('//div[contains(@id,"productDetails")]//tr[contains(th,"ASIN")]/td/text()')
            if node:
                self.adt_asin = node[0].strip()
            elif node2:
                self.adt_asin = node2[0].strip()
            L.debug('AddTime: ASIN remains still')
        except:
            L.debug('AddTime: ASIN remains still')

    def setPhantom(self):
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = (self.ua)
        driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities, service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(40)
        return driver

    def setChrome(self):
        driver = webdriver.Chrome()
        return driver

    # 上架时间
    def add_time(self):
        keepaUrl = 'https://keepa.com/iframe_addon.html#1-0-' + self.asin
        driver = self.setPhantom()
        try:
            driver.get(keepaUrl)
            # L.debug('phantomjs started')
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'priceHistory')))
        except:
            L.info('!! Page loaded timeout or not available asin:%s' % self.asin)
            driver.quit()
            # L.debug('brower closed')
            return "None"
        else:
            con = driver.page_source
            page_selector = etree.HTML(con)
            add_time = page_selector.xpath('//div[@id="graph"]//table//tr[last()]/td[2]/table//tr[last()]/td[2]/text()')
            if add_time:
                addTime = add_time[0].split("(")[1].split(" ")[0]
                L.debug('%s Add time: %s'%(self.asin, addTime))
                driver.quit()
                # L.debug('brower closed')
                return addTime
            else:
                L.info('>> Failed to locate add time node')
                driver.quit()
                # L.debug('brower closed')
                return "None"



if __name__ == '__main__':
        obj = CrawlAddTime('B00512DYKA')
        c = obj.add_time()
        print c
