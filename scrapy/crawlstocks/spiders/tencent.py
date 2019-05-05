#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy
from io import StringIO
from datetime import datetime
from pymongo import MongoClient

from scrapy_splash import SplashRequest
from crawlstocks.items.tencent import TickDetailItem
from crawlstocks.exceptions import DownloadException
from crawlstocks.items.items import CrawlErrorItem
from crawlstocks.utils.common import cookie_dict

class CrawlTickDetailSpider(scrapy.Spider):
    name = 'tencent.tickdetail'

    # allowed_domains = [ 'gu.qq.com', 'stock.gtimg.cn' ]

    debug = False

    custom_settings = {
            'REDIRECT_ENABLED': True,
            'COOKIES_ENABLED': True,
            # 去重过滤
            'DUPEFILTER_CLASS':'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
            'SPIDER_MIDDLEWARES': {
                'crawlstocks.middlewares.spider.CatchExceptionMiddleware': 600,
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
                },
            'DOWNLOADER_MIDDLEWARES': {
                'crawlstocks.middlewares.download.CatchExceptionMiddleware': 600,
                'crawlstocks.middlewares.download.DebugMiddleware': 820,
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
                },
            # 'ITEM_PIPELINES' : {
                # 'crawlstocks.pipelines.db.tencent.TickDetailPipeline': 100,
                # }
            }

    cookies = dict()

    # 对请求的返回进行处理的配置
    meta = {
        # 'dont_merge_cookies': True, # 设置之后没cookies了
        # 'dont_redirect': True,  # 禁止网页重定向
        # 'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def __init__(self, cookiefile=None):
        if cookiefile:
            self.cookies = cookie_dict(cookiefile)
            # self.logger.info(self.cookies)

    def start_requests(self):
        start_url = 'http://gu.qq.com/i'
        headers = {
                "Host": "gu.qq.com",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
                # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                # "Accept-Language": "en-US,en;q=0.7,zh-CN;q=0.3",
                # "Connection": "keep-alive",
                # "Upgrade-Insecure-Requests": 1,
                # "Pragma": "no-cache",
                # "Cache-Control": "no-cache",
                }
        yield SplashRequest(url=start_url,
                method = 'GET',
                callback=self.parse,
                args={'wait': 8.0, 'image': 1},
                headers=headers, cookies=self.cookies,
                meta=self.meta, dont_filter=True)
        # yield scrapy.Request(url=start_url, headers=headers,
                # cookies=self.cookies, meta=self.meta, dont_filter=True)

    def parse(self, response):
        self.logger.info('length = %d' % len(response.body.decode()))
        try:
            with open('/home/lidong/Downloads/cookie.html', 'w', encoding='utf-8') as f:
                s = response.body.decode()
                f.write(str(s))
        except Exception as e:
            print(e)
        # self.logger.info(response.body)
            # browser.find_element_by_xpath('//div[@class="zxg-stocklist"]'), 2)
        # self.logger.info(response.xpath('//div[@class="zxg-stocklist"]'))
        # for x in response.xpath('//div[@class="zxg-stocklist"]'):
            # self.logger.info(x)
        # response.xpath('//*[@id="sh600703"]')

#####################################################################################
