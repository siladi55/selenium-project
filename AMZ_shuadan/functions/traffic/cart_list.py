#coding=utf-8
import setting
import browser as bo
from db.SQLModel import Record2DB
from logs.log import Logger
Log = Logger(__file__)
Rdb = Record2DB()


class Actions(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf

    def select_size_color(self):
        """如果遇到需要选颜色尺寸才能加入购物车的情况再就写个方法"""
        pass

    def add_to_cart(self):
        try:
            self.d.rand_move()
            cart_xp = '//input[@id="add-to-cart-button"]'
            exbox_xp = '//div[@class="a-popover-header"]/button[@aria-label="Close"]'
            if self.d.is_element_exist(cart_xp):
                self.d.move_to_click(cart_xp)
                if self.d.is_element_exist(exbox_xp):
                    self.d.click_opt(exbox_xp)
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加购物车', '成功加入购物车')
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加购物车')
                Log.info('<add to cart>: 成功加入购物车')
                return True
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加购物车', '加入购物车失败，没找到节点')
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加购物车')
                Log.info('<add to cart>: 加入购物车失败，没找到add to cart节点')
                return False
        except:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加购物车', '加入购物车失败')
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加购物车')
            Log.info('<add to cart>: 加入购物车执行失败')
            return False

    def add_to_list(self):
        try:
            self.d.rand_move()
            list_xp = '//input[@id="add-to-wishlist-button-submit"]'
            create_xp = '//form[@class="reg-create-form"]/div[@class="a-form-actions"]/span[last()]//input'
            closebox_xp = '//div[@class="a-popover-header"]/button[@aria-label="Close"]'
            if self.d.is_element_exist(list_xp):
                self.d.move_to_click(list_xp)
                if self.d.is_element_exist(create_xp):
                    self.d.click_opt(create_xp)
                    if self.d.is_element_exist(closebox_xp):
                        self.d.click_opt(closebox_xp)
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加wish list')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加wish list', '添加收藏成功')
                Log.info('<add to list>: 添加收藏成功')
                return True
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加wish list', '添加收藏失败，没找到节点')
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加wish list')
                Log.info('<add to list>: 添加收藏失败，没找到节点')
                return False
        except:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '添加wish list', '添加收藏操作失败')
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '添加wish list')
            Log.info('<add to list>: 添加收藏操作失败')
            return False



if __name__ == '__main__':
    conf = setting.ChromeConf()  # 可传入浏览器参数类，修改设置参数
    driver = bo.Initial_browser(conf).set_chrome()  # 初始化浏览器
    d = bo.Driver(driver)
    d.request('https://www.amazon.com/dp/B071H84S86')
    h = Actions(d)
    h.add_to_list()