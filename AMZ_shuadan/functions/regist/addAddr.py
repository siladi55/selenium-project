#coding=utf-8
import setting
import util
import browser as bo
from db.SQLModel import Record2DB
from logs.log import Logger

Log = Logger(__file__)
Rdb = Record2DB()


def add_address(driver, conf):
    try:
        account_xp = '//a[@id="nav-link-accountList"]'
        addr_xp = '//a[div[@data-card-identifier="Addresses"]]'
        add_addr_xp = '//div[@id="ya-myab-plus-address-icon"]'
        country_xp = '//span[@id="address-ui-widgets-countryCode"]'
        fullname_xp = '//input[@id="address-ui-widgets-enterAddressFullName"]'
        addr_line1 = '//input[@id="address-ui-widgets-enterAddressLine1"]'
        addr_line2 = '//input[@id="address-ui-widgets-enterAddressLine2"]'
        city_xp = '//input[@id="address-ui-widgets-enterAddressCity"]'
        state_xp = '//input[@id="address-ui-widgets-enterAddressStateOrRegion"]'
        zip_code_xp = '//input[@id="address-ui-widgets-enterAddressPostalCode"]'
        phoneNo_xp = '//input[@id="address-ui-widgets-enterAddressPhoneNumber"]'
        add_btn = '//input[@class="a-button-input" and @type="submit"]'
        save_btn = '//input[@name="address-ui-widgets-saveOriginalOrSuggestedAddress"]'
        driver.click_opt(account_xp)
        driver.wait_clickable(addr_xp)
        driver.click_opt(addr_xp)
        driver.wait_clickable(add_addr_xp)
        driver.click_opt(add_addr_xp)
        driver.wait_clickable(country_xp)
        driver.wait(fullname_xp)
        driver.wait(addr_line1)
        driver.wait(addr_line2)
        driver.wait(city_xp)
        driver.wait(state_xp)
        driver.wait(zip_code_xp)
        driver.wait(phoneNo_xp)
        driver.click_opt(country_xp)
        c_us = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="United States"]'
        c_uk = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="United Kingdom"]'
        c_ca = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Canada"]'
        c_jp = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Japan"]'
        c_de = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Germany"]'
        c_fr = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="France"]'
        c_es = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Spain"]'
        c_it = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Italy"]'
        c_au = '//div[@aria-hidden="false" and @data-action="a-popover-a11y"]//li/a[text()="Australia"]'
        map_ = {1: c_us, 2: c_uk, 3: c_ca, 4: c_jp, 5: c_de, 6: c_fr, 7: c_es, 8: c_it, 9: c_au}
        for i in xrange(20):
            util.rand_stay(0.5, 1)
            driver.press_key(country_xp)
            if driver.is_element_exist(map_[conf.addr_cty]):
                driver.click_opt(map_[conf.addr_cty])
                break
        driver.click_opt(fullname_xp)
        util.rand_stay(2, 3)
        driver.send_key(fullname_xp, conf.fullname)
        driver.send_key(addr_line1, conf.streetaddr)
        driver.send_key(city_xp, conf.city)
        driver.send_key(state_xp, conf.state)
        driver.send_key(zip_code_xp, conf.zip_code)
        driver.send_key(phoneNo_xp, conf.phoneNo)
        driver.click_opt(add_btn)
        util.rand_stay()
        if driver.is_element_exist(add_btn):
            driver.move_to_click(add_btn)
            if driver.is_element_exist(add_btn):
                # bo.update_cookie_to_db(driver, conf.guid, conf.user, '邮箱注册', '地址初始化')
                Log.error('地址信息未被Amazon识别，保存失败')
                Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加地址,: 地址信息未被Amazon识别，保存失败')
                Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功，地址信息填写有误'" % conf.guid)
            else:
                Log.error('地址信息未被Amazon识别，但仍保存成功')
                Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加地址: 地址信息未被Amazon识别，强制保存成功')
                Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,地址设置成功'" % conf.guid)
        else:
            if driver.is_element_exist(save_btn):
                driver.click_opt(save_btn)
            Log.info('Succeed to save addr.')
            Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加地址: 地址设置成功')
            Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,地址设置成功'" % conf.guid)
    except Exception, e:
        # bo.update_cookie_to_db(driver, conf.guid, conf.user, '邮箱注册', '地址初始化')
        Log.exc("<add addr> 地址设置失败。(%s)" % e)
        Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加地址: 地址设置失败(请检查操作节点)')
        Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,地址设置失败'" % conf.guid)



