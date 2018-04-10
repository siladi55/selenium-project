#coding=utf-8
import setting
import util
import browser as bo
from db.SQLModel import Record2DB
from logs.log import Logger
from lxml import etree
Log = Logger(__file__)
Rdb = Record2DB()


class Review(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf

    def see_all_reviews(self):
        review_link = '//a[@data-hook="see-all-reviews-link-foot"]'
        if self.d.is_element_exist(review_link):
            self.d.move_to_click(review_link)
            return True
        else:
            Log.error('<see all review>: 未找到see all review节点')
            return False

    def match_review(self, selector):
        reviews_xp = '//div[@data-hook="review"]'
        title = self.conf.review_title
        author = self.conf.review_author
        t_xp = './/a[@data-hook="review-title"]/text()'
        a_xp = './/a[@data-hook="review-author"]/text()'
        for i in selector.xpath(reviews_xp):
            # print i.xpath(t_xp)[0], i.xpath(a_xp)[0]
            if title == i.xpath(t_xp)[0] and author == i.xpath(a_xp)[0]:
                Log.info('找到了评论(title:%s)'%title)
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '找到了评论(title:%s)'%title)
                id_ = i.xpath('./@id')
                return id_[0] if len(id_) else None

    def select_yes_no(self, nodeId):
        assert nodeId is not None, "Node id can't be None"
        try:
            choice = self.conf.review_help
            yes_xp = '//div[contains(@class, "comments-for-{0}")]//span[contains(@class, "cr-vote-yes")]'.format(nodeId)
            no_xp = '//div[contains(@class, "comments-for-{0}")]//span[contains(@class, "cr-vote-no")]'.format(nodeId)
            map_ = {1: yes_xp, 0: no_xp}
            self.d.move_to_click(map_[choice])
            return True
        except:
            return False

    def search_page(self):
        next_xp = '//div[@id="cm_cr-pagination_bar"]//li[last()]'
        end_xp = '//div[@id="cm_cr-pagination_bar"]//li[@class="a-disabled a-last"]'
        while 1:
            selector = etree.HTML(self.d.page_source)
            util.rand_stay(2, 3)
            node = self.match_review(selector)
            if len(selector.xpath(next_xp)):
                if node is not None:
                    return node
                else:
                    self.d.move_to_click(next_xp)
                    # print '查找下一页'
            elif len(selector.xpath(end_xp)):
                return node
            else:
                return node

    def yes_no_opt(self):
        if self.see_all_reviews():
            rv_node = self.search_page()
            if rv_node is not None:
                Log.info('找到评论')
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '找到评论')
                if self.select_yes_no(rv_node):
                    Log.info('评论点赞成功')
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '评论点赞成功')
                    # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '评论', '评论点赞')
                    return True
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '评论点赞失败')
                    # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '评论', '评论点赞')
                    return False
            else:
                Log.info('未找到该评论，请检查:%s' % self.conf.review_title)
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '未找到该评论，请检查(title: %s)' % self.conf.review_title)
                # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '评论', '评论点赞')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '评论', '未找到see all review节点')
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '评论', '评论点赞')
            return False


    def make_comment(self):
        pass



if __name__ == '__main__':
    conf = setting.ChromeConf()  # 可传入浏览器参数类，修改设置参数
    driver = bo.Initial_browser(conf).set_chrome()  # 初始化浏览器
    d = bo.Driver(driver)
    d.request('https://www.amazon.com/dp/B00M1WMFBM')
    h = Review(d)
    h.see_all_reviews()
    review_node = h.search_page()
    print review_node, "node"
    if review_node is not None:
        h.select_yes_no(review_node)
    else:
        print '未找到该评论，请检查评论和xpath'
