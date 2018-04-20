#coding=utf-8
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
import zipfile
from selenium import webdriver
# from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from logs.log import Logger
import browser as bo
from util import *
Log = Logger(__name__)


class Initial_browser(object):
    def __init__(self, bs_conf_obj):
        self.conf = bs_conf_obj

    def set_chrome(self):
        options = webdriver.ChromeOptions()
        # options.add_extension(os.path.join(os.getcwd(), 'chromeExtentions', 'WebRTC Network Limiter_0_2_1_3.crx'))
        options.add_extension(os.path.join(os.getcwd(), 'chromeExtentions', 'WebRTC Control.crx'))
        options.add_extension(os.path.join(os.getcwd(), 'chromeExtentions', 'CanvasFingerprintBlock_1_5.crx'))
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        if not os.path.exists(self.conf.execute_path):
            raise Exception('Please set chromedriver path, or add it into environ path')
        if self.conf.proxy:
            if '@' in self.conf.proxy:
                options.add_extension(self.auth_proxy(*self.conf.proxy.split('@')))
            else:
                options.add_argument('--proxy-server=http://' + self.conf.proxy)
        if self.conf.user_agent:
            options.add_argument('user-agent=' + self.conf.user_agent)
        if not self.conf.showImg:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
        if self.conf.font is not None:
            options.add_argument('lang='+self.conf.font)
        if self.conf.acpt_lang is not None:
            prefs = {'intl.accept_languages': self.conf.acpt_lang}
            options.add_experimental_option('prefs', prefs)
        options.add_argument('disable-infobars')
        options.add_argument('-start-maximized')
        options.add_argument('--disable-java')
        options.add_argument('--disable-webrtc')
        driver = webdriver.Chrome(executable_path=self.conf.execute_path, chrome_options=options)
        driver.set_page_load_timeout(self.conf.timeout)
        driver.maximize_window()
        driver.switch_to.window(driver.window_handles[0])
        return driver

    def auth_proxy(self, host, port, user, pw):
        manifest_json = '''
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            '''

        background_js = '''
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "http",
                        host: "%(host)s",
                        port: parseInt(%(port)d)
                      },
                      bypassList: ["foobar.com"]
                    }
                  };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%(user)s",
                        password: "%(pass)s"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );''' % {
            "host": host,
            "port": port,
            "user": user,
            "pass": pw,
        }
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return pluginfile

    """
        def set_fireFox(self):
        profileDir = r"C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\7eo321rh.default"
        exe_path = r'C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe'
        profile = webdriver.FirefoxProfile(profileDir)
        if self.conf.proxy:
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", self.conf.proxy.split(':')[0])
            profile.set_preference("network.proxy.http_port", self.conf.proxy.split(':')[1])
            profile.set_preference('network.proxy.ssl', self.conf.proxy.split(':')[0])
            profile.set_preference('network.proxy.ssl_port', self.conf.proxy.split(':')[1])
            profile.set_preference("network.proxy.no_proxies_on", "")
        if self.conf.user_agent:
            profile.set_preference('general.useragent.override', self.conf.user_agent)
        profile.set_preference("webdriver_assume_untrusted_issuer", False)
        profile.update_preferences()
        profile.set_preference("media.peerconnection.enabled", False)
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=exe_path)
        driver.maximize_window()
        driver.set_page_load_timeout(self.conf.timeout)
        return driver
    
    def set_phantomjs(self):
        desired_capabilities = webdriver.DesiredCapabilities.PHANTOMJS
        if self.conf.user_agent is not None:
            desired_capabilities["phantomjs.page.settings.userAgent"] = self.conf.user_agent
        if not self.conf.showImg:
            desired_capabilities["phantomjs.page.settings.loadImages"] = self.conf.showImg
        if self.conf.proxy is not None:
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.conf.proxy
            proxy.add_to_capabilities(desired_capabilities)

        driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,
                                     service_args=['--ignore-ssl-errors=true'])
        driver.set_page_load_timeout(self.conf.timeout)
        driver.maximize_window()
        return driver
    """

class Driver(object):
    """default browser is chrome"""
    def __init__(self, driver, dr_conf):
        self.d = driver
        self.conf = dr_conf
        # self.flag = 1

    def quit_opt(self):
        self.d.quit()

    def page_back(self):
        self.d.back()
        rand_stay()

    def to_first_handler(self):
        self.d.switch_to.window(self.d.window_handles[0])

    @property
    def page_source(self):
        return self.d.page_source

    def output_node_text(self, xp):
        try:
            text = self.d.find_element_by_xpath(xp).text
            return str(text).strip()
        except Exception, e:
            Log.exc('<output_node_text>: 节点文本输出失败(%s)' % e)
            return False

    def request(self, url):
        try:
            self.d.get(url)
            rand_stay()
            return True
        except:
            # self.flag = 0
            self.d.execute_script('window.stop()')
            Log.exc('<request>:页面加载超时， 已停止加载')
            return False

    def send_key(self, xp, value):
        try:
            s = self.d.find_element_by_xpath(xp)
            rand_stay(1, 2)
            s.clear()
            for i in value:
                rand_stay(0.1, 0.2)
                s.send_keys(i)
            rand_stay()
        except Exception, e:
            # self.flag = 0
            Log.exc('<send_key>: Not found node: %s(%s)' % (xp, e))

    def click_opt(self, xp):
        try:
            # self.wait_clickable(xp)
            self.d.find_element_by_xpath(xp).click()
            rand_stay()
        except Exception, e:
            # self.flag = 0
            Log.exc('<click_opt>: Not found node: %s(%s)' % (xp, e))

    def wait(self, xp):
        try:
            WebDriverWait(self.d, self.conf.waitime).until(EC.presence_of_element_located((By.XPATH, xp)))
            return True
        except Exception, e:
            # self.flag = 0
            Log.exc("<wait_opt>: Not found node:%s(%s)" % (xp, e))
            return False

    def wait_clickable(self, xp):
        try:
            WebDriverWait(self.d, self.conf.waitime).until(EC.element_to_be_clickable((By.XPATH, xp)))
            return True
        except Exception, e:
            # self.flag = 0
            Log.exc('<wait_clickable>: %s(%s)' % (e, xp))
            return False

    def move_to_node(self, xp, offset=0):
        """Scroll element from head. the element will be moved to the top, adjust according to offset"""
        try:
            y = self.d.find_element_by_xpath(xp).location['y'] - self.conf.page_offset
            i = 0
            while i < y-offset:
                js = "var q=document.documentElement.scrollTop=" + str(i)
                self.d.execute_script(js)
                stay()
                i += int(random.uniform(*self.conf.page_move_rate))
            rand_stay()
        except Exception:
            # self.flag = 0
            Log.exc("<move_to_node>: move to node failed:(%s)" % xp)

    def move_to_click(self, xp, offset=0):
        """Scroll from page head"""
        self.move_to_node(xp, offset=offset)
        self.click_opt(xp)
        rand_stay(3, 5)

    def move_from_to(self, fxp, txp):
        try:
            yf = self.d.find_element_by_xpath(fxp).location['y']
            yt = self.d.find_element_by_xpath(txp).location['y']
            if yf < yt:
                i = yf - self.conf.page_offset
                while i < yt - self.conf.page_offset:
                    js = "var q=document.documentElement.scrollTop=" + str(i)
                    self.d.execute_script(js)
                    stay()
                    i += int(random.uniform(*self.conf.page_move_rate))
                    if i > yt - self.conf.page_offset:
                        i = yt - self.conf.page_offset
            elif yf > yt:
                i = yf - self.conf.page_offset
                while i > yt - self.conf.page_offset:
                    js = "var q=document.documentElement.scrollTop=" + str(i)
                    self.d.execute_script(js)
                    stay()
                    i -= int(random.uniform(*self.conf.page_move_rate))
                    if i < yt - self.conf.page_offset:
                        i = yt - self.conf.page_offset
            rand_stay()
        except Exception, e:
            Log.exc("<move_to_node>: move to node failed: %s(%s)" % (e, txp))

    def move_from_to_click(self, fxp, txp):
        self.move_from_to(fxp, txp)
        self.click_opt(txp)
        rand_stay()

    def jump_to_hold(self, elem):
        ActionChains(self.d).move_to_element(elem).perform()
        rand_stay()

    def jump_to_node(self, xp):
        ele = self.d.find_element_by_xpath(xp)
        ActionChains(self.d).move_to_element(ele).perform()
        rand_stay()

    def jump_to_click(self, xp):
        self.jump_to_node(xp)
        self.click_opt(xp)
        rand_stay()

    def is_element_exist(self, xp):
        # if not (isinstance(xp, str) and len(xp)):
        #     raise Exception('<is_element_exist> Xpath expression should be str, got (%s)' % xp)
        try:
            elem = self.d.find_element_by_xpath(xp)
            return True if elem.is_displayed() and elem.is_enabled() else False
        except:
            return False

    def is_elements_exist(self, xp):
        try:
            elems = self.d.find_elements_by_xpath(xp)
            if len(elems):
                return elems
            return False
        except:
            return False

    def get_elem_counts(self, xp):
        try:
            return len(self.d.find_elements_by_xpath(xp))
        except:
            Log.exc('<get_elem_counts>: 未找到节点[%s]' % xp)
            return 0

    def rand_move(self):
        try:
            i = 0
            while i < random.uniform(*self.conf.rand_move_lenth):
                js = "var q=document.documentElement.scrollTop=" + str(i)
                self.d.execute_script(js)
                stay()
                # rate = random.random()*1000
                # if rate > 992:
                #     rand_stay(1, 2)
                i += int(random.uniform(*self.conf.page_move_rate))
            rand_stay()
            while i > 0:
                js = "var q=document.documentElement.scrollTop=" + str(i)
                self.d.execute_script(js)
                stay()
                # rate = random.random()*1000
                # if rate > 992:
                #     rand_stay(1, 2)
                i -= int(random.uniform(*self.conf.page_move_rate))
            rand_stay()
        except Exception, e:
            # self.flag = 0
            Log.exc("<rand_move>: random move failed: %s" % e)

    def press_key(self, xp, key='down'):
        tem = {'up': Keys.UP,
               'down': Keys.DOWN,
               'enter': Keys.ENTER,
               'tab': Keys.TAB}
        try:
            s = self.d.find_element_by_xpath(xp)
            s.send_keys(tem[key])
        except Exception, e:
            # print 'press key opt'
            Log.exc('<press_key>: Not found node: %s(%s)' % (xp, e))

    def ul_selector(self, ul_xp, dest_xp):
        try:
            ul_box = self.d.find_element_by_xpath(ul_xp)
            ul_box.find_element_by_xpath(dest_xp).click()
            rand_stay()
        except:
            Log.exc('<ul_selector>: 执行错误')


    def select(self, xp, value):
        try:
            rand_stay()
            s1 = Select(self.d.find_element_by_xpath(xp))
            try:
                s1.select_by_value(value)
                rand_stay()
                return True
            except Exception, e:
                Log.exc('<Select>: Not found option node by value: %s(%s)' % (value, e))
                return False
        except Exception, e:
            Log.exc('<Select>: Not found select node: %s(%s)' % (xp, e))
            return False

    def visible(self, xp):
        try:
            elem = self.d.find_element_by_xpath(xp)
            return EC.visibility_of_element_located(elem)
        except:
            return False

    # 以下为cookie处理的方法
    def get_cookies_from_bs(self):
        """ get cookie from current page and record it to db. Use the cookie for next login.
            args: a list contains all info about login email, password and so on
        """
        try:
            ck = self.d.get_cookies()
            newList = []
            for i in ck:
                itemDict = {k: i[k] for k in ('domain', 'name', 'value', 'path', 'expiry') if k in i}
                newList.append(itemDict)
            for ck in newList:
                for k, v in ck.items():
                    if isinstance(v, unicode):
                        ck[k] = v.encode('utf-8')
            cookies = str(newList)
            return cookies
        except Exception, e:
            Log.exc('<get cookie>: Failed to get cookies(%s)' % e)
            return ''

    def add_cookies_to_bs(self, cookielist):
        try:
            for i in cookielist:
                # self.d.add_cookie({k: i[k] for k in ('domain', 'name', 'value', 'path', 'expiry') if k in i})
                self.d.add_cookie({k: i[k] for k in ('domain', 'name', 'value', 'path') if k in i})
            return True
        except Exception, e:
            Log.exc('<add cookies> Failed to add cookies(%s)' % e)
            return False

    def delete_cookies(self):
        try:
            self.d.delete_all_cookies()
        except:
            Log.exc('<delete cookies> Failed to del cookies')

    def refresh_page(self):
        try:
            self.d.refresh()
            return True
        except:
            print 'refresh failed'
            return False


def ini_browser_drive(bs_conf, opt_conf):
    driver = bo.Initial_browser(bs_conf).set_chrome()
    return Driver(driver, opt_conf)


if __name__ == '__main__':
    import setting as s
    D = ini_browser_drive(s.BrowserConf(), s.DriverConf())
    D.request('https//:www.whoer.net')
    while True:
        pass
    # print D.output_node_text('//a[@name="tj_trnews"]')