#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import time
from crawlstocks.browser import Browser
from crawlstocks.utils.common import trycall
from crawlstocks.utils.logger import Logger
import crawlstocks.settings as settings

logger = Logger(os.path.basename(__file__))

def _do_save_cookie(browser):
    logger.info('do save cookie')
    cookies = browser.get_cookies()
    with open(settings.GU_QQ_COOKIES_FILE, "w", encoding='utf-8') as f:
        f.write(json.dumps(cookies))

def _do_load_cookie(browser):
    logger.info('do load cookie')
    cookies = []
    with open(settings.GU_QQ_COOKIES_FILE, 'r', encoding='utf-8') as f:
        cookies = json.loads(f.read())

    for each in cookies:
        browser.delete_cookie(each['name'])
        browser.add_cookie(each)
        # browser.add_cookie({
        #     'domain': '.gu.qq.com',
        #     'name': each['name'],
        #     'value': each['value'],
        #     'path': '/',
        #     'expires': None
        #     })

# 登录
def _do_user_login(browser):
    logger.info('do user login')

    # 进入iframe, 否则元素find不到
    trycall(lambda: browser.switch_to_frame('login-node-qq'), 6)
    trycall(lambda: browser.switch_to_frame('ptlogin_iframe'), 1)

    time.sleep(3)

    b = trycall(lambda:
            browser.find_element_by_xpath('//*[@id="switcher_plogin"]'), 2)
    b.click()

    u = trycall(lambda: browser.find_element_by_xpath('//*[@id="u"]'))
    p = trycall(lambda: browser.find_element_by_xpath('//*[@id="p"]'))
    c = trycall(lambda: browser.find_element_by_xpath('//*[@id="login_button"]'))
    u.clear()
    u.send_keys(settings.GU_QQ_USERNAME)
    p.clear()
    p.send_keys(settings.GU_QQ_PASSWORD)
    c.click()

# 自选股
def _do_stock_list(browser):
    # 回到默认的frame
    trycall(lambda: browser.switch_to_default_content())
    time.sleep(1)
    try:
        logger.info('close i kown')
        browser.find_element_by_css_selector('.g_close').click()
    except Exception as e:
        logger.error(e)

    logger.info('do stock list')
    codes = []
    l = trycall(lambda:
            browser.find_element_by_xpath('//div[@class="zxg-stocklist"]'), 2)
    for e in l.find_elements_by_xpath('//dl[contains(@class, "sline s_ga")]'):
        codes.append(e.get_attribute('id')[2:])

    if len(codes) > 0:
        with open(settings.OPTIONAL_CODES_FILE, "w", encoding='utf-8') as f:
            f.write('\n'.join(codes))

def crawl_tencent_optional():
    logger.info('crawl tencent optional')
    browser = Browser('firefox').get_driver()
    try:
        browser.get('http://gu.qq.com/i')
        _do_load_cookie(browser)
        browser.get('http://gu.qq.com/i')
        try:
            _do_stock_list(browser)
        except:
            _do_user_login(browser)
            _do_save_cookie(browser)
            _do_stock_list(browser)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info('browser quit')
        browser.quit()
