#!/usr/bin/python3
# -*- coding: utf-8 -*-

from crawlstocks.browser import Browser
from crawlstocks.utils.common import trycall
import crawlstocks.settings as settings

import time

# 登录
def _do_user_login(browser):
    u = trycall(lambda: browser.find_element_by_xpath('//*[@id="u"]'))
    p = trycall(lambda: browser.find_element_by_xpath('//*[@id="p"]'))
    c = trycall(lambda: browser.find_element_by_xpath('//*[@id="login_button"]'))
    u.send_keys(settings.GU_QQ_USERNAME)
    p.send_keys(settings.GU_QQ_PASSWORD)
    c.click()

# 自选股
def _do_stock_list(browser):
    l = trycall(browser.find_element_by_xpath('//div[@class="zxg-stocklist"]'))
    for e in l.find_elements_by_xpath('/dl[contains(@class, "sline s_ga")]'):
        print(e.get_attribute('id'))

def crawl_tencent_optional():
    browser = Browser('firefox').driver
    try:
        browser.get('http://gu.qq.com/i/#')
        # 进入iframe, 否则元素find不到
        # trycall(browser.switch_to_frame('login-node-qq'))
        # trycall(browser.switch_to_frame('ptlogin_iframe'))
        # loginbtn = trycall(lambda :
                # browser.find_element_by_xpath('//*[@id="switcher_plogin"]'))
        # if loginbtn:
            # loginbtn.click()
        # _do_user_login(browser)
        time.sleep(20)
        _do_stock_list(browser)
    except Exception as e:
        print(e)
    finally:
        time.sleep(10)
        browser.quit()
#sh600703 //*[@id="sh600703"] /html/body/div[4]/div[2]/div[5]
