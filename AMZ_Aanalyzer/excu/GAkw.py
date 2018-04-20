#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import time, re, random, os
from lxml import etree
from util import Basic
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from log.log import Logger
L = Logger('task.GA')

INFODICT = {}


class Login(object):
    def __init__(self, keyword, cid, email='hotdamnet@gmail.com', pw='asdf123456', proxy=None):
        self.keyword = keyword
        self.countryId = cid
        self.country = self.tellCtry(cid)
        self.email = email
        self.pw = pw
        self.ua = random.choice(Basic().USER_AGENT)
        self.proxy = proxy

    def setChromeDriver(self):
        chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=http://' + self.proxy)
        # options.add_argument('user-agent=' + self.ua)
        # options.add_argument('lang=en_US.UTF-8')
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        # os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
        driver.set_page_load_timeout(40)
        driver.maximize_window()
        return driver

    def setPhantomDriver(self):
        desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        desired_capabilities["phantomjs.page.settings.userAgent"] = self.ua
        desired_capabilities["phantomjs.page.settings.resourceTimeout"] = 200000
        desired_capabilities["phantomjs.page.settings.loadImages"] = True
        desired_capabilities["phantomjs.page.settings.disk-cache"] = True
        # desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # 设置phantomjs代理
        # proxy = webdriver.Proxy()
        # proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = self.proxy
        # proxy.add_to_capabilities(desired_capabilities)
        driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities, service_args=['--ignore-ssl-errors=true'])
        # driver.start_session(desired_capabilities)
        # driver.set_page_load_timeout(30)
        driver.maximize_window()
        return driver

    def tellCtry(self, cid):
        if cid == 1:
            return 'United States'
        elif cid == 2:
            return 'United Kingdom'
        elif cid == 3:
            return 'Canada'
        elif cid == 4:
            return 'Japan'
        elif cid == 5:
            return 'Germany'
        elif cid == 7:
            return 'Spain'
        else:
            L.info('Wrong country id')

    # 模拟人工操作
    def operation(self):
        # driver = self.setPhantomDriver()
        driver = self.setChromeDriver()
        try:
            print '>> Requesting login page...'
            driver.get('https://adwords.google.com/um/signin?dst=/ko/KeywordPlanner/Home')  # GA后台管理页
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'identifierId')))
            driver.find_element_by_id('identifierNext')
            print '>> Login Page loaded'
        except Exception as e:
            print e
            print '!! Failed to load login page'
            driver.quit()
            return 0
        else:
            print 'Inputting email...'
            driver.find_element_by_id('identifierId').send_keys(self.email)
            time.sleep(2)
            # 输入帐号密码提交
            print '>> Click NEXT...'
            driver.find_element_by_xpath('//div[@id="identifierNext"]').click()
            time.sleep(2)
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
                print 'Inputting password...'
                driver.find_element_by_id('passwordNext')
            except Exception as e:
                print e
                print '!! Failed to load password page'
                driver.quit()
                return 0
            else:
                driver.find_element_by_xpath('//input[@name="password"]').send_keys(self.pw)
                time.sleep(1)
                driver.find_element_by_id('passwordNext').click()
                # 这里可能会出现验证码，账号输入太频繁咯
                print 'Login Success'
                time.sleep(5)

                try:
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                        (By.ID, 'gwt-debug-splash-panel-search-selection-input')))
                    print '填选页出现'
                    time.sleep(3)
                except Exception as e:
                    print e
                    print '!! Failed to load adwords page'
                    driver.quit()
                    return 0
                else:
                    driver.find_element_by_id('gwt-debug-splash-panel-search-selection-input').click()
                    time.sleep(3)
                    try:
                        # 填关键词节点
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'gwt-debug-keywords-text-area')))
                        xpat = '//div[@id="gwt-debug-splash-panel"]/div[3]/div[2]/div[2]/div/div[4]/div[2]/div[1]'
                        # 国家选择节点
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat)))
                    except Exception as e:
                        print e
                        print 'Failed to click adwords button'
                        driver.quit()
                        return 0
                    else:
                        # 输入要查询的关键字 //div[@id="gwt-debug-splash-panel"]/div[3]/div[2]/div[2]/div/div[4]/div[2]/div[1]
                        driver.find_element_by_id('gwt-debug-keywords-text-area').send_keys(self.keyword)
                        time.sleep(2)
                        driver.find_element_by_xpath(xpat).click()
                        try:
                            # 定位RemoveAll节点
                            rm = '//div[@id="gwt-debug-positive-targets-table"]/table//tr/td[last()]/a'
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, rm)))
                            # 点击removeall 节点
                            driver.find_element_by_xpath(rm).click()
                            # 定位国家填选框
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'gwt-debug-geo-search-box')))
                            save = '//div[@class="gwt-PopupPanel sps-c"]//div[@class="spyb-c"]/div[1]'
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, save)))
                            time.sleep(1)
                        except Exception, e:
                            print e
                            print '!!!!!!!!!!United States，United Kingdom，Germany，Japan，Spain'
                            driver.quit()
                            return 0
                        else:
                            driver.find_element_by_id('gwt-debug-geo-search-box').send_keys(self.country)
                            time.sleep(1)
                            driver.find_element_by_id('gwt-debug-geo-search-box').send_keys(Keys.ENTER)
                            time.sleep(1)
                            driver.find_element_by_xpath(save).click()
                            time.sleep(1)
                            driver.find_element_by_id('gwt-debug-search-button-content').click()
                            time.sleep(7)

                            try:  # 判断下载按钮出现，出现表示数据请求成功，否则就点击get ideas循环4次直到数据出现
                                for i in range(1, 5):
                                    dbtn = '//div[@class="spMb-A" and @style!="display: none;"]/div[@id="gwt-debug-search-download-button"]'
                                    s = driver.find_elements_by_xpath(dbtn)
                                    if len(s):
                                        break
                                    else:
                                        # get ideas 按钮
                                        driver.find_element_by_xpath(
                                            '//div[@id="gwt-debug-search-button" and @style]').click()
                                        time.sleep(i*5)
                                print 'showing'
                            except Exception as e:
                                print e
                                print 'fail'
                                driver.quit()
                                return 0
                            else:
                                print "saving data...."
                                infofile = 'info.html'
                                if os.path.exists(infofile):
                                    os.remove(infofile )
                                with open('temp.txt', 'w') as f:
                                    f.write(driver.page_source)
                                print "30 条数据写入完毕1"
                                self.abstract_kw(infofile )

                                nextpage = '//div[@id="gwt-debug-idea-paging-next" and @aria-disabled="false"]//span[@id="gwt-debug-idea-paging-next-content"]'
                                for i in range(2):
                                    try:
                                        menu = driver.find_element_by_xpath(nextpage)
                                        print '找到第%s页节点' % (i+2)
                                        ActionChains(driver).move_to_element(menu).perform()
                                        driver.find_element_by_xpath(nextpage).click()
                                        time.sleep(3)
                                        with open('temp.txt', 'w') as f:
                                                       f.write(driver.page_source)
                                        print "文件写入完毕%s" % (i+2)
                                        self.abstract_kw(infofile )
                                    except Exception, e:
                                        print e
                                driver.quit()
                                return 1

    def abstract_kw(self, infofile ):
        with open('temp.txt', 'r') as f:
            con = f.read()

        p = '''(<div class="spwd-a" id="gwt-uid-.+?<div class="spcf-a"></div> </div></div></div></div>) <div class="spWc-l" id="gwt-debug-expanded-bundle-table"'''
        info = re.findall(p, con, re.S)
        with open(infofile , 'a') as fa:
            fa.write(info[0])

    def parse_kw(self, kw):
        global INFODICT
        with open('info.html', 'r') as f:
            con = f.read()
        selector = etree.HTML(con)
        kwnode = '//table[@style="width: 284px;"]/tbody[1 and @style!="display: none;"]'
        rankRange = '//table[@id="gwt-debug-middleTable"]/tbody[1 and @style!="display: none;"]'
        kw_nodes = selector.xpath(kwnode)
        range_nodes = selector.xpath(rankRange)
        print len(kw_nodes)
        print len(range_nodes)
        r = 1
        for node in kw_nodes:
            row = node.xpath('./tr')
            kwXpath = './td/div/div/div/span/text()'
            if len(row) > 1:
                for i in row:
                    kw = i.xpath(kwXpath)
                    if len(kw):
                        INFODICT[r] = [kw[0], self.countryId]
                    else:
                        INFODICT[r] = ["None", self.countryId]
                    r += 1
        r = 1
        for item in range_nodes:
            row = item.xpath('./tr')
            rXpath = './td[1]/div/div/text()'
            if len(row) > 1:
                for item in row:
                    rang = item.xpath(rXpath)
                    if len(rang):
                        ran =rang[0].split(' ')
                        val = ran[0] + '-' + ran[-1]
                        INFODICT[r].append(val)
                    else:
                        INFODICT[r].append(-1)
                    r += 1
        for raw in kw_nodes:
            row = raw.xpath('./tr')
            kwXpath = './td/div/div/div/span/text()'
            if len(row) == 1:
                kw = row[0].xpath(kwXpath)
                if len(kw):
                    INFODICT[0] = [kw[0], self.countryId]
                else:
                    INFODICT[0] = ["None", self.countryId]
                break

        for raw in range_nodes:
            row = raw.xpath('./tr')
            rXpath = './td[1]/div/div/text()'
            if len(row) == 1:
                rang = row[0].xpath(rXpath)
                if len(rang):
                    ran =rang[0].split(' ')
                    val = ran[0] + '-' + ran[-1]
                    INFODICT[0].append(val)
                else:
                    INFODICT[0].append(-1)
                break
        if 0 in INFODICT.keys():
            return INFODICT
        else:
            INFODICT[0] = [kw, self.countryId, "None"]
            return INFODICT


def exact_rank(keydict):
    h_url = 'https://keywordseverywhere.com/service/1/getKeywordData.php?apiKey=f25175fb85eab1e502bb&country=&currency=&source=gkplan'
    k_urls = {}
    j = 0
    for i in range(1, 6):
        k_url = ''
        while j < 20*i:
            if j in keydict.keys():
                if isinstance(keydict[j][0], str):
                    k_url += '&kw%5B%5D=' + keydict[j][0].strip().replace(' ', '+')
                else:
                    L.error('wrong kw: %s' % keydict[j])
            else:
                break
            j += 1
        t_url = '&t=%s' % int(round(time.time() * 1000))
        url = h_url + k_url + t_url
        k_urls[i] = url
    print k_urls
    headers = Basic().HEADERS
    headers['Host'] = 'keywordseverywhere.com'
    headers['User-Agent'] = random.choice(Basic().USER_AGENT)
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'

    for i in range(1, 6):
        res = requests.get(k_urls[i], headers=headers, verify=False)
        if res.status_code == 200:
            dt = res.json()
            print dt
            for j in range(20):
                if 20*(i-1)+j in keydict.keys():
                    keydict[20*(i-1)+j].append(dt["data"][str(j)]['vol'])
                else:
                    break
    # print json.dumps(keydict, ensure_ascii=False)
    return keydict



def num_from_kw(kw):
    h_url = 'https://keywordseverywhere.com/service/1/getKeywordData.php?apiKey=f25175fb85eab1e502bb&country=&currency=&source=gkplan'
    k_url = '&kw%5B%5D=' + kw.strip().replace(' ', '+')
    t_url = '&t=%s' % int(round(time.time() * 1000))
    url = h_url + k_url + t_url
    headers = Basic().HEADERS
    headers['Host'] = 'keywordseverywhere.com'
    headers['User-Agent'] = random.choice(Basic().USER_AGENT)
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    res = requests.get(url, headers=headers, verify=False)
    if res.status_code == 200:
        dt = res.json()
        return dt["data"][0]['vol']
    return -1

def main(kw, cid): # 传入关键词和国家
    global INFODICT
    INFODICT = {}
    if isinstance(cid, int):
        obj = Login(kw, cid)
        obj.operation()
        keydict = obj.parse_kw(kw)
        dataDict = exact_rank(keydict)
        print dataDict
        return dataDict
    else:
        print '传入的国家编号有问题'



if __name__ == '__main__':
    # ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    # main('iphone', 1)
    # exact_rank('s')  United States  United Kingdom  Canada  Germany   Spain  Japan
    # d = {0: ['Keyword', 'Avg. Monthly Searches (exact match only)', 'Competition'], 1: ['hat', '100K~1M', '0.80'], 2: ['mens hats', '10K~100K', '1.00'], 3: ['fedora hat', '10K~100K', '1.00'], 4: ['mens caps', '1K~10K', '1.00'], 5: ['caps for men', '1K~10K', '1.00'], 6: ['bucket hat', '10K~100K', '1.00'], 7: ['beanie hats for men', '1K~10K', '1.00'], 8: ["men's hats", '1K~10K', '1.00'], 9: ['blackhat', '10K~100K', '0.57'], 10: ['mens hat styles', '1K~10K', '1.00'], 11: ['hats and caps', '100~1K', '0.99'], 12: ['mens dress hats', '1K~10K', '1.00'], 13: ['cap hat', '1K~10K', '1.00'], 14: ['hats for sale', '1K~10K', '1.00'], 15: ['hats online', '100~1K', '0.89'], 16: ['strapback hats', '1K~10K', '1.00'], 17: ['cool hats for men', '1K~10K', '1.00'], 18: ['cool hats', '10K~100K', '1.00'], 19: ['summer hats', '1K~10K', '1.00'], 20: ['beach hat', '10K~100K', '1.00'], 21: ['mens winter hats', '10K~100K', '1.00'], 22: ['fashion hats', '1K~10K', '1.00'], 23: ['hat man', '1K~10K', '0.99'], 24: ['fedora hats for men', '10K~100K', '1.00'], 25: ['felt hat', '1K~10K', '1.00'], 26: ['beanie hat', '10K~100K', '1.00'], 27: ['hat store', '10K~100K', '0.33'], 28: ['hat shop', '1K~10K', '0.19'], 29: ['flat caps for men', '1K~10K', '1.00'], 30: ['sun hats for men', '10K~100K', '1.00'], 31: ['hat styles', '1K~10K', '1.00'], 32: ['mens straw hats', '10K~100K', '1.00'], 33: ['wide brim hat', '1K~10K', '1.00'], 34: ['mens hats for sale', '100~1K', '1.00'], 35: ['gents hats', '100~1K', '1.00'], 36: ['mens summer hats', '1K~10K', '1.00'], 37: ['hat stores near me', '10K~100K', '0.76'], 38: ['wool hat mens', '1K~10K', '1.00'], 39: ['mens fashion hats', '1K~10K', '1.00'], 40: ['womens hat', '1K~10K', '1.00'], 41: ['mens hat stores near me', '1K~10K', '1.00'], 42: ['types of hats for men', '1K~10K', '1.00'], 43: ['dress hats', '1K~10K', '1.00'], 44: ['mens hats online', '100~1K', '1.00'], 45: ['buy hats', '100~1K', '1.00'], 46: ['mens top hats', '1K~10K', '1.00'], 47: ['mens fedora', '1K~10K', '1.00'], 48: ['mens caps online', '10~100', '1.00'], 49: ['curved hats', '100~1K', '1.00'], 50: ['mens designer hats', '1K~10K', '1.00'], 51: ['cool hats for guys', '1K~10K', '1.00'], 52: ['hat websites', '100~1K', '0.73'], 53: ['mens caps and hats', '100~1K', '1.00'], 54: ['mens wooly hats', '10~100', '1.00'], 55: ['hat shop near me', '1K~10K', '0.68'], 56: ['best beanies for men', '100~1K', '1.00'], 57: ['mens black hat', '1K~10K', '1.00'], 58: ['mens floppy hat', '1K~10K', '1.00'], 59: ['stylish mens hats', '100~1K', '1.00'], 60: ['curved caps', '10~100', '1.00'], 61: ['mens beach hat', '1K~10K', '1.00'], 62: ['mens hat store', '1K~10K', '1.00'], 63: ['mens trilby hats', '100~1K', '1.00'], 64: ['trucker hats for men', '1K~10K', '1.00'], 65: ['mens casual hats', '100~1K', '1.00'], 66: ['mens wide brim hats', '1K~10K', '1.00'], 67: ['curved brim hats', '100~1K', '1.00'], 68: ['mens strapback hats', '100~1K', '1.00'], 69: ['cute dad hats', '100~1K', '1.00'], 70: ['best hats for men', '100~1K', '1.00'], 71: ['best hats', '1K~10K', '0.99'], 72: ['cool hats for sale', '100~1K', '1.00'], 73: ['designer dad hats', '100~1K', '1.00'], 74: ['mens cap styles', '100~1K', '1.00'], 75: ['hats for guys', '1K~10K', '0.95'], 76: ['nice hats for guys', '100~1K', '1.00'], 77: ['mens headwear', '100~1K', '1.00'], 78: ['hats near me', '1K~10K', '0.97'], 79: ['woolen caps for mens', '100~1K', '1.00'], 80: ['mens hats 2016', '100~1K', '1.00'], 81: ['mens caps sale', '100~1K', '1.00'], 82: ['cool beanies for men', '100~1K', '1.00'], 83: ['cool baseball caps for men', '100~1K', '1.00'], 84: ['buy hats online', '100~1K', '1.00'], 85: ['strapback baseball caps', '10~100', '1.00'], 86: ['cool hats for women', '100~1K', '1.00'], 87: ["man's hat", '100~1K', '1.00'], 88: ['hat shop online', '100~1K', '0.94'], 89: ['cool caps for guys', '100~1K', '1.00'], 90: ['stylish hats for guys', '10~100', '1.00'], 91: ['baseball hats near me', '100~1K', '0.96'], 92: ['where to buy hats', '100~1K', '0.85'], 93: ['cool beanies for guys', '100~1K', '1.00'], 94: ['mens leather hats', '1K~10K', '1.00'], 95: ['mens fashion caps', '100~1K', '1.00'], 96: ['sports hats for men', '100~1K', '1.00'], 97: ['best caps for men', '100~1K', '1.00'], 98: ['strapback baseball hats', '100~1K', '1.00'], 99: ['trendy hats for guys', '10~100', '1.00'], 100: ['pink hats for guys', '100~1K', '1.00']}
    # exact_rank(d)
    # obj = Login('knife', 'United States')
    # obj.operation()
    # obj.parse_kw()
    # kdict = {0: ['phone', 'United States', u'100K-1M'], 1: ['mobile phones', 'United States', u'100K-1M'], 2: ['smartphone', 'United States', u'10K-100K'], 3: ['mobiles', 'United States', u'1K-10K'], 4: ['cell phone', 'United States', u'100K-1M'], 5: ['phones for sale', 'United States', u'10K-100K'], 6: ['i phone', 'United States', u'100K-1M'], 7: ['new phone', 'United States', u'10K-100K'], 8: ['new mobile phones', 'United States', u'100-1K'], 9: ['cell phone deals', 'United States', u'10K-100K'], 10: ['mobile phone deals', 'United States', u'1K-10K'], 11: ['mobile phones prices', 'United States', u'100-1K'], 12: ['latest phones', 'United States', u'1K-10K'], 13: ['cheap cell phones', 'United States', u'10K-100K'], 14: ['prepaid phones', 'United States', u'10K-100K'], 15: ['4g mobile phones', 'United States', u'100-1K'], 16: ['mobile phones for sale', 'United States', u'100-1K'], 17: ['latest mobile phones', 'United States', u'100-1K'], 18: ['cell phones for sale', 'United States', u'10K-100K'], 19: ['cheap phones', 'United States', u'10K-100K'], 20: ['mobile price', 'United States', u'100-1K'], 21: ['best phone', 'United States', u'10K-100K'], 22: ['new mobile', 'United States', u'100-1K'], 23: ['cell phone plans', 'United States', u'10K-100K'], 24: ['unlock phone', 'United States', u'100K-1M'], 25: ['latest mobile', 'United States', u'100-1K'], 26: ['cheap mobile phones', 'United States', u'100-1K'], 27: ['phone deals', 'United States', u'10K-100K'], 28: ['contract phones', 'United States', u'1K-10K'], 29: ['best mobile phone deals', 'United States', u'100-1K'], 30: ['buy mobile phones', 'United States', u'100-1K'], 31: ['phone shop', 'United States', u'1K-10K'], 32: ['best mobile phone', 'United States', u'1K-10K'], 33: ['new cell phones', 'United States', u'1K-10K'], 34: ['mobile phone plans', 'United States', u'1K-10K'], 35: ['phone plans', 'United States', u'10K-100K'], 36: ['flip phone', 'United States', u'10K-100K'], 37: ['all mobile phones', 'United States', u'100-1K'], 38: ['unlocked cell phones', 'United States', u'10K-100K'], 39: ['best cell phone plans', 'United States', u'10K-100K'], 40: ['best mobile', 'United States', u'1K-10K'], 41: ['mobile phones online', 'United States', u'100-1K'], 42: ['mobile phone contracts', 'United States', u'100-1K'], 43: ['phone price', 'United States', u'1K-10K'], 44: ['compare mobile phones', 'United States', u'100-1K'], 45: ['cell phone prices', 'United States', u'1K-10K'], 46: ['new smartphones', 'United States', u'1K-10K'], 47: ['buy phones', 'United States', u'1K-10K'], 48: ['best cell phone', 'United States', u'10K-100K'], 49: ['unlocked mobile phones', 'United States', u'1K-10K'], 50: ['best cell phone deals', 'United States', u'10K-100K'], 51: ['cellphones', 'United States', u'10K-100K'], 52: ['cheap cell phone plans', 'United States', u'10K-100K'], 53: ['mobile shop', 'United States', u'1K-10K'], 54: ['prepaid cell phones', 'United States', u'10K-100K'], 55: ['all phones', 'United States', u'1K-10K'], 56: ['cell phone companies', 'United States', u'10K-100K'], 57: ['wireless phone', 'United States', u'1K-10K'], 58: ['mobile phone shops', 'United States', u'1K-10K'], 59: ['buy cell phones', 'United States', u'1K-10K'], 60: ['top 10 mobile phones', 'United States', u'100-1K'], 61: ['cheap phones for sale', 'United States', u'1K-10K'], 62: ['3g phone', 'United States', u'100-1K'], 63: ['all phone price', 'United States', u'10-100'], 64: ['compare phones', 'United States', u'10K-100K'], 65: ['latest cell phones', 'United States', u'100-1K'], 66: ['mobile handset', 'United States', u'10-100'], 67: ['cell phone shop', 'United States', u'1K-10K'], 68: ['mobile phone offers', 'United States', u'100-1K'], 69: ['upcoming mobile phones', 'United States', u'100-1K'], 70: ['buy mobile online', 'United States', u'100-1K'], 71: ['cheap mobile phone deals', 'United States', u'10-100'], 72: ['good mobile phones', 'United States', u'10-100'], 73: ['cheap unlocked phones', 'United States', u'1K-10K'], 74: ['top mobile phones', 'United States', u'100-1K'], 75: ['cheap mobile phones for sale', 'United States', u'10-100'], 76: ['online phone shopping', 'United States', u'100-1K'], 77: ['flip mobile phones', 'United States', u'100-1K'], 78: ['all smartphones', 'United States', u'100-1K'], 79: ['cheap phone deals', 'United States', u'100-1K'], 80: ['cdma mobile phone', 'United States', u'100-1K'], 81: ['prepaid cell phone plans', 'United States', u'1K-10K'], 82: ['refurbished mobile phones', 'United States', u'100-1K'], 83: ['cheap mobile deals', 'United States', u'10-100'], 84: ['compare mobile phone deals', 'United States', u'10-100'], 85: ['cell phone providers', 'United States', u'1K-10K'], 86: ['cell phone carriers', 'United States', u'1K-10K'], 87: ['discount cell phones', 'United States', u'1K-10K'], 88: ['t mobile cell phones', 'United States', u'10K-100K'], 89: ['which mobile phone', 'United States', u'10-100'], 90: ['buymobiles', 'United States', u'100-1K']}
    # exact_rank(kdict)
    num_from_kw("mop")