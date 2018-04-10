#coding=utf-8
import setting
import util
import browser as bo
from db.SQLModel import Record2DB
from logs.log import Logger
from lxml import etree
Log = Logger(__file__)
Rdb = Record2DB()


class QA(object):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf

    def _match_question(self, selector):
        # question_xp = '//div[contains(@id,"question-")]'
        # question = setting.CONF2['question']
        # text_xp = './div/div[2]/a/text()'
        # for i in selector.xpath(question_xp):
        #     if question.strip() == i.xpath(text_xp)[0].strip().replace('  ', ' '):
        #         print 'mathched'
        #         qa_id = i.xpath('./@id')
        #         return qa_id[0] if len(qa_id) else None
        question_id = self.conf.question_id
        question_xp = '//div[@id="question-{0}"]'.format(question_id)
        if len(selector.xpath(question_xp)):
            return question_id

    def _search_from_deep_pages(self):
        next_xp = '//div[@id="askPaginationBar"]//li[last()]'
        end_xp = '//div[@id="askPaginationBar"]//li[@class="a-disabled a-last"]'
        while 1:
            selector = etree.HTML(self.d.page_source)
            util.rand_stay(2, 3)
            qa_id = self._match_question(selector)

            if len(selector.xpath(end_xp)):
                if not qa_id:
                    print 'Failed to match question'
                    break
                else:
                    return qa_id
            elif len(selector.xpath(next_xp)):
                if not qa_id:
                    self.d.move_to_click(next_xp)
                else:
                    print 'matched question'
                    return qa_id
            else:
                print 'cant find next or end xpath'
                return qa_id

    def _search_all_qa(self):
        btn1_xp = '//span[contains(@class, "askSeeMoreQuestionsLink")]'
        btn2_xp = '//span[contains(@class, "askLoadMoreQuestionsLink")]'
        btn3_xp = '//div[contains(@class, "askLoadMoreQuestions")]/a'
        selector = etree.HTML(self.d.page_source)
        qa_id0 = self._match_question(selector)
        if not qa_id0:
            if len(selector.xpath(btn1_xp)):
                self.d.jump_to_click(btn1_xp)
                selector = etree.HTML(self.d.page_source)
                qa_id1 = self._match_question(selector)
                if not qa_id1:
                    if len(selector.xpath(btn2_xp)):
                        self.d.jump_to_click(btn2_xp)
                        selector = etree.HTML(self.d.page_source)
                        qa_id2 = self._match_question(selector)
                        if not qa_id2:
                            if len(selector.xpath(btn3_xp)):
                                self.d.jump_to_click(btn3_xp)
                                return self._search_from_deep_pages()
                            else:
                                Log.info('当前qa少于12, 且没匹配到question')
                        else:
                            Log.info('已匹配到question')
                            return qa_id2
                    else:
                        Log.info('当前qa少于8, 且没匹配到question')
                else:
                    Log.info('已匹配到question')
                    return qa_id1
            else:
                Log.info('当前qa少于4,且没匹配到question')
        else:
            Log.info('已匹配到question')
            return qa_id0

    def search(self):
        review_xp = '//h2[@id="dp-customer-review-header"]'
        self.d.move_to_node(review_xp)
        print '等待qa加载出来。。。'
        util.rand_stay(1, 2)
        qa_id = self._search_all_qa()
        if qa_id:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '找到提问(id:%s)' % self.conf.question_id)
            return qa_id
        else:
            Log.info('未找到提问：%s' % self.conf.question_id)
            Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '未找到提问(id:%s)' % self.conf.question_id)

    def vote(self, qa_id):
        try:
            vote_xp = '//div[./div[2]/div[@id="question-{0}"]]/div[1]'.format(qa_id)
            vote_up = vote_xp + '/ul/li[1]/form/input[last()]'
            vote_down = vote_xp + '/ul/li[last()]/form/input[last()]'
            map_ = {1: vote_up, 0: vote_down}
            xp = map_[self.conf.vote]
            self.d.move_to_node(vote_xp)
            util.rand_stay(2, 4)
            self.d.click_opt(xp)
            Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', 'vote投票成功')
            return True
        except:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', 'vote投票失败')
            return False

    def answer_yes_no(self, qa_id):
        try:
            question_xp = '//div[@id="question-{0}"]/div/div[2]/a'.format(qa_id)
            self.d.move_to_click(question_xp)
            answer_id = self.conf.answerer_id
            chose = self.conf.answer_help
            next_xp = '//div[@id="askPaginationBar"]//li[last() and @class="a-last"]'
            end_xp = '//div[@id="askPaginationBar"]//li[last() and @class="a-disabled a-last"]'
            yes_xp = '//form[@id="askVoteHelpfulForm-{0}"]'.format(answer_id)
            no_xp = '//form[@id="askVoteUnHelpfulForm-{0}"]'.format(answer_id)
            map_ = {1:yes_xp, 2:no_xp}
            xp = map_[chose]
            while 1:
                selector = etree.HTML(self.d.page_source)
                util.rand_stay(2, 3)
                if len(selector.xpath(end_xp)):
                    if len(selector.xpath(xp)):
                        self.d.move_to_click(xp)
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞成功')
                        return True
                    else:
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '未找到回答（id:%s' % self.conf.answerer_id)
                        return False
                elif len(selector.xpath(next_xp)):
                    if len(selector.xpath(xp)):
                        self.d.move_to_click(xp)
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞成功')
                        return True
                    else:
                        self.d.click_opt(next_xp)
                else:
                    if len(selector.xpath(xp)):
                        self.d.move_to_click(xp)
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞成功')
                        return True
                    else:
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '未找到回答（id:%s' % self.conf.answerer_id)
                        return False
        except:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞失败')
            return False


    def vote_opt(self):
        qa_id = self.search()
        if qa_id:
            tmp = self.vote(qa_id)
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, 'QA问答', 'vote 投票')
            return tmp
        else:
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, 'QA问答', 'vote 投票')
            return False

    def yes_no_opt(self):
        qa_id = self.search()
        if qa_id:
            tmp = self.answer_yes_no(qa_id)
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞')
            return tmp
        else:
            # bo.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, 'QA问答', '问答点赞')
            return False


if __name__ == '__main__':
    conf = setting.ChromeConf()  # 可传入浏览器参数类，修改设置参数
    driver = bo.Initial_browser(conf).set_chrome()  # 初始化浏览器
    d = bo.Driver(driver)
    d.request('https://www.amazon.com/dp/B077Y8DN87')
    h = QA(d)
    qid = h.search()
    if qid:
        print '1'
        h.answer_yes_no(qid)
    else:
        print qid, 'qid'
