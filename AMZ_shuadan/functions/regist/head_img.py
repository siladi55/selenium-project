#coding=utf-8
import os
import util
import SendKeys
import browser as bo
from logs.log import Logger
from db.SQLModel import Record2DB
Log = Logger(__file__)
Rdb = Record2DB()


def add_profile(driver, conf):
    try:
        account = '//a[@id="nav-link-accountList"]'
        profile_xp = '//div[@data-card-identifier="OrderingAndShoppingPreferences"]//a[contains(@href, "profile")]'
        add_btn_xp = '//div[@id="pr-upload-button"]/div[2]//img'
        notnow_xp = '//span[./span[@id="a-autoid-0-announce"]]'
        sub_xp = '//span[./span[@id="a-autoid-3-announce"]]'
        edit_xp = '//a[contains(@href, "edit_activity_settings")]'
        add_btn2 = '//div[contains(@class, "image-edit-popover-trigger-holder")]'
        upload_xp = '//label[@class="imageUploadLabel"]'
        close_xp = '//button[@data-action="a-popover-close"]'
        bio_xp = '//textarea[@id="profile_personal_description"]'
        fb_xp = '//input[@id="profile_social_facebook"]'
        twitter_xp = '//input[@id="profile_social_twitter"]'
        youtube_xp = '//input[@id="profile_social_youtube"]'
        pint_xp = '//input[@id="profile_social_pinterest"]'
        instagram_xp = '//input[@id="profile_social_instagram"]'
        save_xp = '//span[@data-pr-edit]/span[@id="save-public-activity"]'
        driver.click_opt(account)
        driver.move_to_node(profile_xp)
        driver.click_opt(profile_xp)
        if os.path.exists(conf.imgPath):
            if driver.is_element_exist(notnow_xp):  # 第一种情况，从没上传过头像的页面
                driver.click_opt(add_btn_xp)
                SendKeys.SendKeys(r'' + conf.imgPath)
                util.rand_stay(2, 3)
                SendKeys.SendKeys("{ENTER}")
                util.rand_stay(2, 3)
                driver.click_opt(sub_xp) #?AMZ 有问题， 提交不了的话点notNow
            else:  # 曾经上传过头像的页面
                driver.click_opt(add_btn2)
                driver.click_opt(upload_xp)
                SendKeys.SendKeys(r'' + conf.imgPath)
                SendKeys.SendKeys("{ENTER}")
            Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加画像: 头像图片添加成功')
        else:
            Log.error('<add profile>: Wrong image path, it does not exist.')
            Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加画像: 头像图片添加失败，请检查路径')
        util.rand_stay(5, 6)
        #
        if driver.is_element_exist(close_xp):
            driver.click_opt(close_xp)
        driver.click_opt(edit_xp)
        driver.send_key(bio_xp, conf.bio)
        driver.send_key(fb_xp, conf.fb)
        driver.send_key(twitter_xp, conf.twitter)
        driver.send_key(youtube_xp, conf.youtube)
        driver.send_key(pint_xp, conf.pint)
        driver.send_key(instagram_xp, conf.instagram)
        driver.click_opt(save_xp)
        if driver.flag:
            Log.info("Profile modification finished")
            # bo.update_cookie_to_db(driver, conf.guid, conf.user, '邮箱注册', '画像初始化')
            Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加画像: 画像修改成功, 资料已初始化')
            Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,资料已初始化'" % conf.guid)
        else:
            # bo.update_cookie_to_db(driver, conf.guid, conf.user, '邮箱注册', '画像初始化')
            Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加画像: 画像修改失败')
            Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,添加画像失败'" % conf.guid)
    except Exception, e:
        # bo.update_cookie_to_db(driver, conf.guid, conf.user, '邮箱注册', '画像初始化')
        Log.exc("<add profile>: 画像添加失败。(%s)" % e)
        Rdb.insert_log(conf.guid, conf.user, '邮箱注册', '添加画像: 画像修改失败')
        Rdb.callProc("exec sys_InsertAccount '%s',2,'注册成功,添加画像失败'" % conf.guid)

