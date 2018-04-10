#coding=utf-8
import sys
import re
import browser, time
from setting import *
import db.get_params_from_db as g
from util import rand_stay
from db.SQLModel import Record2DB
from logs.log import Logger
reload(sys)
sys.setdefaultencoding('utf-8')
L = Logger(__file__)
Rdb = Record2DB()


class Shopping(object):
    # def __init__(self, driver, conf, addrConf, cardConf):
    def __init__(self, driver, conf):
        self.d = driver
        self.conf = conf
        if conf.newAddrGuid:
            self.addrConf = AddrConf(g.addr_params(conf.newAddrGuid, usage='deliver'))
        else:
            self.addrConf = AddrConf()
        self.cardConf = CardConf(g.card_params(self.addrConf.fullname, conf.ccard_guid, conf.giftcard_guid))

    def _add_to_cart(self):
        try:
            L.info('<search seller>: 非跟卖，点击加入购物车')
            self.d.rand_move()
            cart_xp = '//input[@id="add-to-cart-button"]'
            exbox_xp = '//div[@class="a-popover-header"]/button[@aria-label="Close"]'
            ctn2add_xp = '//form[@id="smartShelfFormContinue"]//input[@value="addToCart"]'
            if self.d.is_element_exist(cart_xp):
                self.d.jump_to_click(cart_xp)
                if self.d.is_element_exist(exbox_xp):
                    self.d.click_opt(exbox_xp)
                elif self.d.is_element_exist(ctn2add_xp):
                    self.d.click_opt(ctn2add_xp)
                    L.info('<add to cart>: Continue to add success')
                return True
            else:
                L.error('<add to cart>: 未找到加入购物车按钮')
                return False
        except:
            L.error('<add to cart>: 加入购物车失败')
            return False

    def _search_seller(self):
        try:
            L.info('<search seller>: 选择跟卖')
            buy_cart_xp = '//div[@id="olp_feature_div"]/div/span[1]/a'
            if self.d.is_element_exist(buy_cart_xp):
                sellerNo = self.d.output_node_text(buy_cart_xp)
                print 'seller No', sellerNo
                if sellerNo:
                    quantity = re.findall('\((.*?)\)', sellerNo)
                    quantity = int(quantity[0])
                    if quantity > 1:
                        self.d.move_to_click(buy_cart_xp)
                        next_xp = '//li[@class="a-last"]'
                        end_xp = '//li[@class="a-disabled a-last"]'
                        while 1:
                            addcart_xp = '//div[./div/h3/span/a[contains(@href,"%s")]]/div[last()]' \
                                         '//form//input[@name="submit.addToCart"]' % self.conf.shop_id
                            # fba_xp = '//div[./div/h3/span/a[contains(@href, "%s")]]/div[3]/div' % self.conf.shop_id
                            fba_addcart_xp = '//div[./div/h3/span/a[contains(@href,"%s")] and ./div[3]/div]' \
                                             '/div[last()]//form//input[@name="submit.addToCart"]' % self.conf.shop_id
                            nofba_addcart_xp = '//div[./div/h3/span/a[contains(@href,"%s")] and not(./div[3]/div)]' \
                                               '/div[last()]//form//input[@name="submit.addToCart"]' % self.conf.shop_id
                            if self.d.is_element_exist(addcart_xp):
                                if self.conf.fba == 1:
                                    if self.d.is_element_exist(nofba_addcart_xp):
                                        self.d.move_to_click(nofba_addcart_xp)
                                        L.info('跟卖非FBA加入购物车成功')
                                        return True
                                elif self.conf.fba == 2:
                                    if self.d.is_element_exist(fba_addcart_xp):
                                        self.d.move_to_click(fba_addcart_xp)
                                        L.info('跟卖FBA加入购物车成功')
                                        return True
                                else:
                                    L.error('跟卖发货方式参数有误')
                                    return False
                            if not self.d.is_element_exist(next_xp):
                                L.info('<search_seller>: 当前页面仅一页，且未匹配到')
                                return False
                            elif self.d.is_element_exist(end_xp):
                                L.info('<search_seller>: 最后一页，未找到跟卖商家')
                                return False
                            else:
                                self.d.move_to_click(next_xp)
                    else:
                        L.error('<search_seller>: 跟卖商家为1，无需跟卖，请重新设置参数')
                        return False
                else:
                    L.error('<search_seller>: 跟卖商家数正则没匹配到')
                    return False
            else:
                L.error('<search_seller>: 没找到跟卖节点')
                return False
        except Exception, e:
            L.exc('<search seller>: 执行错误（%s）' % e)
            return False

    def _clear_cart(self):
        try:
            cart_xp = '//a[@id="nav-cart"]'
            items_xp = '//form[@id="activeCartViewForm"]/div[@data-name="Active Items"]'
            del2_xp = items_xp + '/div[2]/div[@class="sc-list-item-content"]//input[@value="Delete"]'
            del3_xp = items_xp + '/div[3]/div[@class="sc-list-item-content"]//input[@value="Delete"]'
            self.d.click_opt(cart_xp)
            time.sleep(2)
            while 1:
                if self.d.is_element_exist(del2_xp):
                    self.d.click_opt(del2_xp)
                    time.sleep(4)
                elif self.d.is_element_exist(del3_xp):
                    self.d.click_opt(del3_xp)
                    time.sleep(4)
                else:
                    break
            L.info('<clear cart>: 已清除购物车其他商品')
            return True
        except:
            L.info('<clear cart>: 清除购物车其他商品失败')
            return False

    def _checkout(self):
        """结算点击完判断一次，如果失败再点击结算"""
        try:
            ct_xp = '//div[@id="huc-v2-order-row-container"]//a[@id="hlb-ptc-btn-native"]'
            ct_xp2 = '//input[@name="proceedToCheckout"]'
            ct_xp3 = '//*[@id="hlb-ptc-btn-bottom"]//a[@id="hlb-ptc-btn-native-bottom"]'
            if self.d.is_element_exist(ct_xp):
                self.d.click_opt(ct_xp)
                L.info('<checkout>: 开始结算')
                if self.d.is_element_exist(ct_xp):
                    rand_stay()
                    self.d.click_opt(ct_xp)
                return True
            elif self.d.is_element_exist(ct_xp2):
                self.d.click_opt(ct_xp2)
                L.info('<checkout>: 开始结算')
                if self.d.is_element_exist(ct_xp2):
                    rand_stay()
                    self.d.click_opt(ct_xp2)
                return True
            elif self.d.is_element_exist(ct_xp3):
                self.d.move_to_click(ct_xp3)
                L.info('<checkout>: 开始结算')
                if self.d.is_element_exist(ct_xp3):
                    rand_stay()
                    self.d.move_to_click(ct_xp3)
                return True
            else:
                L.info('<checkout>: 结算失败')
                return False
        except:
            return False

    def _place_direct(self):
        place_xp = '//input[@name="placeYourOrder1"]'
        return True if self.d.is_element_exist(place_xp) else False

    def whether_change_addr(self):
        change_xp = '//div[./strong[text()="Shipping address"]]/span/a'
        add_new_xp = '//div[@id="spc-popover-add-new-address-link"]/a'
        if self.d.is_element_exist(change_xp):
            self.d.click_opt(change_xp)
            time.sleep(4)
            if self.d.is_element_exist(add_new_xp):
                self.d.click_opt(add_new_xp)
                return True
            else:
                L.error('<change addr>: 未找到add new addr 节点')
                return False
        else:
            L.error('<change addr>: 未找到change 节点')
            return False

    def whether_change_ccard(self):
        change_xp = '//a[@id="payment-change-link"]'
        if self.d.is_element_exist(change_xp):
            self.d.click_opt(change_xp)
            return True
        else:
            L.error('<change ccard>: 未找到change 节点')
            return False

    def whether_gift_card(self):
        try:
            text_xp = '//input[@id="spc-gcpromoinput"]'
            apply_xp = '//input[@value="Apply"]'
            if self.d.is_element_exist(text_xp):
                self.d.send_key(text_xp, self.cardConf.gift_code)
                self.d.click_opt(apply_xp)
                L.info('<gift card>: 礼品卡添加完毕')
                return True
            else:
                L.info('<gift card>: 礼品卡添加失败，没找到填卡节点')
                return False
        except:
            L.info('<gift card>: 礼品卡添加执行失败')
            return False

    def _check_login(self):
        map_ = {1: 'Sign in', 2: "Sign in", 3: "Sign in", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
        login_xp = '//h1[contains(text(), "%s")]' % map_[self.conf.cid]
        if self.d.is_element_exist(login_xp):
            L.info('<check_login>: 购买登陆状态无效，需重新登陆')
            sub_xpath = '//input[@id="signInSubmit"]'
            p_xpath = '//input[@id="ap_password"]'
            self.d.wait_clickable(sub_xpath)
            self.d.send_key(p_xpath, self.conf.pw)
            self.d.click_opt(sub_xpath)
            if self.d.is_element_exist(sub_xpath):
                L.error('<login> 登录失败, 请检查原因')
                return False
            else:
                L.info('<check login>: 购买刷单,登录成功')
                return True
        else:
            L.debug('<check_login>: 登陆状态有效，无需重登界面')
            return True
    """
    由于要获取发货地址收件人姓名作为信用卡的持卡人姓名，此处全部采用填写新地址，并将新地址收件人传给信用卡人
    def _to_exist_addr(self):
        try:
            addr_xp = '//div[contains(@id, "address-book-entry")]/div[contains(@class, "ship-to-this-address")]//a'
            if self.d.is_element_exist(addr_xp):
                self.d.click_opt(addr_xp)
                L.info('<exist_addr>: 送货到已有地址,点击成功')
                return True
            else:
                L.info('<exist_addr>: 未找到已有地址节点')
                return False
        except:
            L.exc('<exist_addr>: 送货到已有地址点击失败')
            return False
    """

    def _to_new_addr(self):

        fullname_xp = '//div[@id="enterAddressFullNameContainer"]//input'
        addr1_xp = '//div[@id="enterAddressAddressLine1Container"]//input'
        addr2_xp = '//div[@id="enterAddressAddressLine2Container"]//input'
        city_xp = '//div[@id="enterAddressCityContainer"]//input'
        state_xp = '//div[@id="enterAddressStateOrRegionContainer"]//input'
        zip_xp = '//div[@id="enterAddressPostalCodeContainer"]//input'
        cty_xp = '//div[@id="enterAddressCountryCodeContainer"]//select'
        phoneNo_xp = '//div[@id="enterAddressPhoneNumberContainer"]//input'
        sub_xp = '//input[@type="submit" and @name="shipToThisAddress"]'
        addr_error_xp = '//div[@id="addressIMB"]//h4'
        cty_map = {1: 'US', 2: 'GB', 3: 'CA', 4: 'JP', 5: 'DE', 6: 'FR', 7: 'ES', 8: 'IT', 9: 'AU'}
        try:
            if self.d.is_element_exist(fullname_xp):
                self.d.wait(fullname_xp)
                self.d.wait(addr1_xp)
                self.d.wait(addr2_xp)
                self.d.wait(city_xp)
                self.d.wait(state_xp)
                self.d.wait(zip_xp)
                self.d.wait(phoneNo_xp)
                self.d.wait_clickable(sub_xp)
                self.d.wait_clickable(cty_xp)
                self.d.send_key(fullname_xp, self.addrConf.fullname)
                self.d.send_key(addr1_xp, self.addrConf.streetaddr)
                self.d.send_key(city_xp, self.addrConf.city)
                self.d.send_key(state_xp, self.addrConf.state)
                self.d.send_key(zip_xp, self.addrConf.zip_code)
                self.d.click_opt(cty_xp)
                self.d.select(cty_xp, cty_map[self.addrConf.addr_cty])
                self.d.send_key(phoneNo_xp, self.addrConf.phoneNo)
                self.d.click_opt(sub_xp)
                if self.d.is_element_exist(addr_error_xp):
                    L.error('<to_new_addr>: 新地址未被AMZ识别，添加失败')
                    return False
                else:
                    L.error('<to_new_addr>: 新地址添加成功')
                    return True
            else:
                L.error('<to_new_addr>: 新地址填写节点未找到')
                return False
        except Exception, e:
            L.exc('<to_new_addr>: 新地址添加失败(%s)' % e)
            return False

    def _submit_continue(self):
        try:
            ctn_xp = '//form[@id="shippingOptionFormId"]/div[1]//div/div/span[1]/span/input[@type="submit"]'
            if self.d.is_element_exist(ctn_xp):
                self.d.click_opt(ctn_xp)
                return True
            else:
                L.error('<submit_continue>: 提交发货方式失败(%s)')
                return False
        except:
            return False

    def _by_ccard_info(self):
        add_new_xp = '//div[@id="new-payment-methods"]//a[@data-expander-content="new-cc"]'
        ccname_xp = '//input[@id="ccName"]'
        ccNo_xp = '//input[@id="addCreditCardNumber"]'
        mon_btn_xp = '//span[.//select[@id="ccMonth"]]//button[@role="button"]'
        mon_ul_xp = '//div[@id="a-popover-1"]//ul'
        mon_opt_xp = mon_ul_xp + '/li[{0}]/a'.format(self.cardConf.exp_mon)
        year_btn_xp = '//span[.//select[@id="ccYear"]]//button[@role="button"]'
        year_ul_xp = '//div[@id="a-popover-2"]//ul'
        year_opt_xp = year_ul_xp + '/li[{0}]/a'.format(self.cardConf.exp_year)
        add_cart_xp = '//input[@id="ccAddCard"]'
        error_xp = '//div[@id="newCCErrors" and @style]'
        try:
            print 'cccard---:', self.cardConf
            if not self.d.is_element_exist(ccname_xp):
                if self.d.is_element_exist(add_new_xp):
                    self.d.click_opt(add_new_xp)
                else:
                    print '[add a card] 节点未找到'
            if self.d.is_element_exist(ccname_xp):
                self.d.send_key(ccname_xp, self.cardConf.ccname)
                self.d.send_key(ccNo_xp, self.cardConf.ccNo)
                self.d.press_key(ccNo_xp, 'tab')
                time.sleep(2)
                self.d.click_opt(mon_btn_xp)
                self.d.ul_selector(mon_ul_xp, mon_opt_xp)
                time.sleep(2)
                self.d.click_opt(year_btn_xp)
                self.d.ul_selector(year_ul_xp, year_opt_xp)
                self.d.click_opt(add_cart_xp)
                time.sleep(1)
                if self.d.is_element_exist(error_xp):
                    L.error('<ccard info>: 信用卡添加失败，请检查卡信息')
                    return False
                else:
                    L.info('<ccard info>: 信用卡添加成功')
                    return True
            else:
                L.error('<ccard info>: 信用卡填写节点未找到，请检查代理')
                return False
        except:
            L.error('<ccard info>: 信用卡添加操作失败')
            return False

    def _by_gift_card(self,):
        gift_btn = '//a[@id="gc-link-expander"]'
        code_text_xp = '//div[@id="new-giftcard-promotion" and @style="display: block;"]' \
                       '//input[@id="gcpromoinput"]'
        apply_xp = '//div[@id="new-giftcard-promotion" and @style="display: block;"]' \
                   '//input[@id="button-add-gcpromo"]'
        error_xp = '//div[@id="new-giftcard-promotion" and @style="display: block;"]' \
                   '//div[@id="gcpromoerrorblock" and @style="display: block;"]'
        try:
            print 'giftcard---:', self.cardConf
            if self.d.is_element_exist(gift_btn):
                self.d.click_opt(gift_btn)
                self.d.send_key(code_text_xp, self.cardConf.gift_code)
                self.d.click_opt(apply_xp)
                if self.d.is_element_exist(error_xp):
                    L.error('<gift card>:礼品卡添加失败, 请检查卡信息')
                    return False
                else:
                    L.info('<gift card>:礼品卡添加成功')
                    return True
            else:
                L.error('<gift card>:礼品卡节点未找到, 请检查网络，或节点xpath')
                return False
        except:
            L.error('<gift card>:礼品卡添加操作失败')
            return False

    def _submit_card(self):
        try:
            ctn_xp = '//div[@id="order-summary-container"]//input[@id="continue-top"]'
            if self.d.is_element_exist(ctn_xp):
                self.d.click_opt(ctn_xp)  # 提交
                return True
            else:
                L.error('无法提交卡信息， continue disable')
                return False
        except:
            return False

    def _free_shipping(self):
        try:
            free_xp = '//div[@id="primeAutomaticPopoverAdContent"]//a[@rel="nt1"]'
            no_xp = '//span[@id="mom-no-thanks"]/a'
            if self.d.is_element_exist(free_xp):
                self.d.click_opt(free_xp)
                L.info('<free shipping>: [no thanks]点击成功')
                return True
            elif self.d.is_element_exist(no_xp):
                self.d.click_opt(no_xp)
                L.info('<free shipping>: [no thanks]点击成功')
                return True
            else:
                L.info('<free shipping>: 未找到[no thanks]节点, 无会员试用广告')
                return False
        except:
            L.info('<free shipping>: [free shipping]操作失败')
            return False

    def _billing_addr(self):
        try:
            addr_xp = '//div[contains(@id, "address-book-entry")]/div[contains(@class, "ship-to-this-address")]//a'
            if self.d.is_element_exist(addr_xp):
                self.d.click_opt(addr_xp)
                L.info('<billing_addr>: 账单地址点击成功')
                return True
            else:
                L.info('<billing_addr>: 未找到账单地址节点')
                return False
        except:
            L.exc('<billing_addr>: 账单地址点击失败')
            return False

    def _place_order(self):
        try:
            sum_price_xp = '//div[@id="subtotals-marketplace-table"]/table//tr[last()]/td[last()]/strong'
            place_xp = '//div[@id="right-grid"]//input[@name="placeYourOrder1"]'
            if self.d.is_element_exist(place_xp):
                self.d.click_opt(place_xp)
                L.info('<place order>: 订单提交成功')
                return self.d.output_node_text(sum_price_xp)
            else:
                L.info('<place order>: 未找到订单提交按钮')
                return False
        except:
            L.exc('<place order>: 订单提交失败')
            return False

    def _record_order(self, sum_):
        try:
            track_xp = '//span[contains(@id,"order-number-")]'
            track_no = self.d.output_node_text(track_xp)
            if Rdb.sum_trackno(self.conf.task_guid, sum_, track_no):
                L.info('<订单总价及追踪号入库成功>')
                return True
            else:
                L.info('<订单总价及追踪号入库失败>')
                return False
        except:
            L.info('<订单总价及追踪号入库执行失败>')
            return False

    def proceed_checkout(self):
        # 判断是否跟卖
        if self.conf.buy_cart == 1:
            if self._search_seller():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '跟卖添加购物车成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '跟卖添加购物车失败')
                return False
        elif self.conf.buy_cart == 0:
            if self._add_to_cart():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '添加购物车成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '添加购物车失败')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '未获取到跟卖指令参数')
            return False
        # 清除购物车其他商品
        if self._clear_cart():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购物车其他商品已清除')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购物车其他商品清除失败')
        # 点击结算
        if self._checkout():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '开始结算')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '未找到结算按钮，结算失败')
            return False
        return self.after_checkout2() if self._place_direct() else self.after_checkout1()

    def after_checkout1(self):
        # 登录
        if self._check_login():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购买登录成功')
            browser.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '购买刷单')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购买登录状态无效，登录失败')
            return False
        # 判断是否添加新地址
        if self.conf.newAddrGuid:  # 添加新地址有值且不为空
            if self._to_new_addr():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '发货新地址添加成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '发货新地址添加失败')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '没传发货地址GUID')
            L.error('<new addr>: 没传发货地址GUID')
            return False
        # 提交发货方式
        if self._submit_continue():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '提交发货方式成功')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '提交发货方式失败')
            return False
        # 添加卡信息
        if self.conf.ccard_guid and not self.conf.giftcard_guid:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '仅添加信用卡')
            if self._by_ccard_info():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加失败')
                return False
        elif self.conf.giftcard_guid and not self.conf.ccard_guid:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '仅添加礼品卡')
            if self._by_gift_card():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加失败')
                return False
        elif self.conf.giftcard_guid and self.conf.ccard_guid:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '添加信用卡和礼品卡')
            if self._by_ccard_info():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加成功')
                if self._by_gift_card():
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡和礼品卡都添加成功')
                    L.info("<proceed_checkout>: 卡填写完毕")
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加失败')
                    return False
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加失败')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '没有卡信息参数，无法添加任何卡')
            L.error("<proceed_checkout>: 没有卡信息参数，无法添加任何卡")
            return False
        # 提交卡信息
        if self._submit_card():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交成功')
            L.info("<proceed_checkout>: 卡提交成功")
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交失败')
            L.info("<proceed_checkout>: 卡提交失败")
            return False
        # 添加账单地址
        if self._billing_addr():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址提交成功')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址没找到，无需提交')
        # 无需fast free shipping
        if self._free_shipping():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '无需fast free shipping点击成功')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '无fast free shipping')
        # 提交订单
        total = self._place_order()
        if total:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单提交成功')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址提交失败')
            return False
        if self._record_order(total):
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单总价及追踪号入库成功')
            return True
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单总价及追踪号入库失败')
            return False

    def after_checkout2(self):
        """点击checkout 按钮之后可能会出现直接下单的页面，
        地址和卡信息得点击Change去修改，此函数做此种情况的购买
        """
        # 登录
        if self._check_login():
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购买登录成功')
            browser.update_cookie_to_db(self.d, self.conf.task_guid, self.conf.user, '购买刷单')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '购买登录状态无效，登录失败')
            return False
        # 改发货地址
        if self.whether_change_addr():
            self._to_new_addr()
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '发货新地址添加失败')
            return False
        time.sleep(5)
        # 添加卡信息
        if self.conf.ccard_guid and not self.conf.giftcard_guid:
            if self.whether_change_ccard():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '仅添加信用卡')
                if self._by_ccard_info():
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加成功')
                    # 提交卡信息
                    if self._submit_card():
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交成功')
                        L.info("<proceed_checkout>: 卡提交成功")
                    else:
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交失败')
                        L.info("<proceed_checkout>: 卡提交失败")
                        return False
                    # 添加账单地址
                    if self._billing_addr():
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址提交成功')
                    else:
                        Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址没找到，无需提交')
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加失败')
                    return False
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '修改信用卡失败')
                return False
        elif self.conf.giftcard_guid and not self.conf.ccard_guid:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '仅添加礼品卡')
            if self.whether_gift_card():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加成功')
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加失败')
                return False
        elif self.conf.giftcard_guid and self.conf.ccard_guid:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '添加信用卡和礼品卡')
            if self._by_ccard_info():
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加成功')
                # 提交卡信息
                if self._submit_card():
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交成功')
                    L.info("<proceed_checkout>: 卡提交成功")
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '卡提交失败')
                    L.info("<proceed_checkout>: 卡提交失败")
                    return False
                # 添加账单地址
                if self._billing_addr():
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址提交成功')
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址没找到，无需提交')
                time.sleep(4)
                if self._by_gift_card():
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡和礼品卡都添加成功')
                    L.info("<proceed_checkout>: 卡填写完毕")
                else:
                    Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '礼品卡添加失败')
                    return False
            else:
                Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '信用卡添加失败')
                return False
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '没有卡信息参数，无法添加任何卡')
            L.error("<proceed_checkout>: 没有卡信息参数，无法添加任何卡")
            return False

        # 提交订单
        total = self._place_order()
        if total:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单提交成功')
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '账单地址提交失败')
            return False
        if self._record_order(total):
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单总价及追踪号入库成功')
            return True
        else:
            Rdb.insert_log(self.conf.task_guid, self.conf.user, '购买刷单', '订单总价及追踪号入库失败')
            return False




if __name__ == '__main__':
    pass



