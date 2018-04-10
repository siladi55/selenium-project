#coding=utf-8
import random
from util import CidTransfer, rand_stay
from db.SQLModel import Record2DB
from logs.log import Logger
Log = Logger(__file__)
Rdb = Record2DB()


class InnerTraffic(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf
        self.flag = 0

    def index_page(self):
        url = 'https://' + CidTransfer(self.conf.cid).value
        self.d.request(url)

    def search_by_kw(self):
        try:
            search_xp = '//input[@id="twotabsearchtextbox"]'
            go = '//input[@value="Go"]'
            # if self.d.is_element_exist(search_xp):
            self.d.send_key(search_xp, self.conf.kw)
            self.d.click_opt(go)
            return True
        except:
            Log.error('<search by kw>: 搜索产品页面未加载出来')
            return False

    def search_by_cata(self, ):
        try:
            if len(self.conf.option_value):
                select_cata = '//select[@id="searchDropdownBox"]'
                if self.d.is_element_exist(select_cata):
                    value = self.conf.option_value
                    rand_stay(2, 3)
                    self.d.select(select_cata, value)
                    return True
                else:
                    Log.error('<search_by_cata>: 父类目节点未找到，页面未加载出来')
                    return False
            else:
                Log.info('<search by cata>: 未收到父类目设置参数，父类目将不做设置')
                return True
        except:
            Log.error('<search_by_cata>: 未找到父类目节点')
            return False

    def search_by_sub_cata(self):
        try:
            if len(self.conf.cata):
                cate_xp = '//li//a[contains(string(.), "{0}")]'.format(self.conf.cata)
                if self.d.is_element_exist(cate_xp):
                    self.d.click_opt(cate_xp)
                    return True
                else:
                    Log.error('<search_by_sub_cata>: Not found catalog: %s' % self.conf.cata)
                    return False
            else:
                Log.info('<search by subcata>: 未收到子类目设置参数，子类目将不做设置')
                return True
        except:
            Log.error('<search_by_sub_cata>: 子类目节点点击失败')
            return False

    def search_by_price(self):
        try:
            if len(self.conf.search_price):
                lprice = '//input[@id="low-price"]'
                hprice = '//input[@id="high-price"]'
                go = '//span[input[@value="Go"]]'
                de_go = '//span[input[@value="Los"]]'
                fr_go = '//span[input[@value="Aller"]'
                es_go = '//span[input[@value="Ir"]'
                it_go = '//span[input[@value="Vai"]'
                map_ = {1:go, 2:go, 3:go, 5:de_go, 6:fr_go, 7:es_go, 8:it_go, 9:go}
                if self.d.is_element_exist(lprice):
                    self.d.move_to_node(lprice)
                    self.d.click_opt(lprice)
                    self.d.send_key(lprice, str(self.conf.search_price[0]))
                    self.d.click_opt(hprice)
                    self.d.send_key(hprice, str(self.conf.search_price[1]))
                    self.d.click_opt(map_[self.conf.cid])
                    Log.info('<search_by_price>: 价格筛选成功')
                else:
                    Log.info('<search_by_price>: 未找到价格节点, 将忽略价格筛选')
            else:
                Log.info('<search_by_price>: 未收到价格筛选参数，将忽略价格筛选')
            return True
        except:
            Log.error("<search_by_price>: 价格节点输入失败")
            return False

    # def match_asin(self):
        # con = self.d.page_source
        # pattern = '(https://(.){1,100}/dp/' + self.conf.asin + '/.+?)">'
        # try:
            # url = re.search(pattern, con).group(1)
            # print "matched url!!!!", url
        # if self.product_xpath() is not None:
        #     return True
            # return self.product_xpath(url)
        # else:
        #     return False
        # except:
        #     return False

    def match_by_xpath(self):
        """默认剔除推广链接，返回自然排名的产品xpath"""
        ignore_sponsored = self.conf.ignore_sponsored
        # url0 = url.split("?")[0].split('=')[0]
        # node = '//li[contains(@id, "result_") and ./div/div[last()]/div//a[contains(@href, "{0}")]]'.format(url0)
        node = '//li[contains(@id, "result_") and @data-asin="{0} and .//div.h5"]'.format(self.conf.asin.upper())
        ignore_node = '//li[contains(@id, "result_") and @data-asin="{0}" and not(.//div/h5)]'.format(self.conf.asin.upper())
        # ignore_node = '//li[contains(@id, "result_") and .//*[contains(@href, "{0}")] and not(.//div/h5)]'.format(url0)
        if ignore_sponsored:
            return ignore_node if self.d.is_element_exist(ignore_node) else None
        else:
            return node if self.d.is_element_exist(node) else None

    def detail_page(self, goods_node):
        try:
            rand_stay()
            self.d.move_to_node(goods_node)
            goods_xp = goods_node + '/div/div/div//img[1]'
            # print 'goods_xp', goods_xp 假设产品总会有图片连接到产品页
            self.d.click_opt(goods_xp)
            Log.info('<detail page>: 进入到产品页：%s' % self.conf.asin)
            return True
        except:
            Log.exc("<detail_page>: 进入产品详细页失败")
            return False

    def random_scan(self, i):
        """选取第4-10个产品中随机一个"""
        ran = random.choice(range(3, 11))
        goods_node = '//li[contains(@id, "result_{0}")]'.format(ran)
        if self.detail_page(goods_node):
            Log.info('随机进入第%s页产品(%s)' % (i, goods_node))
            return goods_node + '/div/div/div//img[1]'
        Log.info('随机进入第%s页产品(%s)失败' % (i, ran))

    def search_in_pages(self):
        """Search product in specified pages. Return product url"""
        for i in range(self.conf.search_page):
            print 'search in pages:i', i
            goods_xp = self.match_by_xpath()
            if goods_xp:
                Log.info('找到产品：%s' % self.conf.asin)
                self.flag = 1
                return goods_xp
            else:
                rand_goods = self.random_scan(i)
                if rand_goods is not None:
                    self.d.rand_move()
                    rand_stay()
                    self.d.page_back()
                    rand_stay()
                    self.d.move_from_to_click(fxp=rand_goods, txp='//a[@id="pagnNextLink"]')
                else:
                    self.d.move_to_click(txp='//a[@id="pagnNextLink"]')
        if not self.flag:
            Log.info('未找到产品：%s' % self.conf.asin)

    def search(self):
        print '4', self.conf.task_guid
        if self.search_by_cata():
            print 'c1'
            if self.search_by_kw():
                print 'k1'
                if self.search_by_sub_cata():
                    print 'sc2'
                    if self.search_by_price():
                        print 'p1'
                        goods_xp = self.search_in_pages()
                        if goods_xp:
                            print 'g1'
                            Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品',
                                           '找到产品(asin:%s)' % self.conf.asin)
                            if self.detail_page(goods_xp):
                                print 'd1'
                                Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品', '进入产品页(asin:%s)' % self.conf.asin)
                                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '站内流量查找产品')
                                return True
                            else:
                                Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品', '进入产品页失败')
                                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '站内流量查找产品')
                                return False
                        else:
                            Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品',
                                           '未找到产品(asin:%s)' % self.conf.asin)
                            Log.info('goods_xp 为空：%s' % goods_xp)
                            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '站内流量查找产品')
                            return False
                    else:
                        return False
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品', '子类目操作失败')
                    return False
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品', '关键词输入失败')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '站内流量查找产品', '父类目操作失败')
            return False


if __name__ == '__main__':

    t.index_page()
    # t.search_by_cata(value="search-alias=amazon-devices")
    t.search_by_kw('ipad')
    # print t.match_asin()
    # t.click_next_page()
    # t.search_by_nav_cata('Fire Tablets')
    # print '1'
    # url = t.search_process()
    # print url
    # print '2'
    # if url:
    #     xp = t.product_xpath(url)
    #     print '3'
    #     print xp
        # xp = xp + '//a[contains(@href, "https://www.amazon.com/Fnova-Protective-Absorption-Cushion-Resistant/dp/B075NV8BCK/ref")]'
    t.search_by_price()
        # t.detail_page(xp)
    # else:
    #     print 'weizhaodao'
        # while 1: pass
