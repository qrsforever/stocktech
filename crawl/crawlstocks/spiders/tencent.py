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
from crawlstocks.utils.common import trans_cookie

class CrawlTickDetailSpider(scrapy.Spider):
    name = 'tencent.tickdetail'
    allowed_domains = [ 'gu.qq.com', 'stock.gtimg.cn', 't.10jqka.com.cn',
    'stockpage.10jqka.com.cn', 'upass.10jqka.com.cn', 'www.10jqka.com.cn']

    debug = False

    # start_urls = ['http://gu.qq.com/i/']
    start_urls = ['http://upass.10jqka.com.cn/login']

    # custom_settings = {
    #         'DUPEFILTER_CLASS':'scrapy_splash.SplashAwareDupeFilter',
    #         'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
    #         'SPIDER_MIDDLEWARES': {
    #             'crawlstocks.middlewares.spider.CatchExceptionMiddleware': 600,
    #             'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    #             },
    #         'DOWNLOADER_MIDDLEWARES': {
    #             'crawlstocks.middlewares.download.CatchExceptionMiddleware': 600,
    #            'scrapy_splash.SplashCookiesMiddleware': 723,
    #            'scrapy_splash.SplashMiddleware': 725,
    #            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    #             },
    #         'ITEM_PIPELINES' : {
    #             'crawlstocks.pipelines.db.tencent.TickDetailPipeline': 100,
    #             }
    #         }
    
    cookies = None
    
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def __init__(self, cookiefile=None):
        if cookiefile:
           try:
               with open(cookiefile, 'r', encoding='utf-8') as f:
                   self.cookies = trans_cookie(f.readline())
                   self.logger.info(self.cookies)
           except:
               self.logger.info("open file:%s error!" % cookiefile)

    def start_requests(self):
        url = 'http://upass.10jqka.com.cn/login'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
                url = url,
                formdata = {"uname" : "985612771@qq.com", "passwd" : "861808"},
                callback = self.parse)
        # start_url = 'http://gu.qq.com/i/'
        # headers = {
        #         "Host": "gu.qq.com",
        #         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
        #         # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #         "Accept-Language": "en-US,en;q=0.7,zh-CN;q=0.3",
        #         # "Accept-Encoding": "gzip, deflate",
        #         "Connection": "keep-alive",
        #         "Upgrade-Insecure-Requests": 1,
        #         "Pragma": "no-cache",
        #         "Cache-Control": "no-cache",
        #         'Connection': 'keep-alive',
        #         }
        #   # yield SplashRequest(url=start_url,
        #           # callback=self.parse,
        #           # args={'wait': 3.0},
        #           # headers=headers, cookies=self.cookies,
        #           # meta=self.meta
        #           # )
        # yield scrapy.Request(url=start_url,headers=headers, cookies=self.cookies, meta=self.meta)

    def parse(self, response):
        self.logger.info(response.url)
        yield scrapy.Request(url = 'http://t.10jqka.com.cn/newcircle/user/userPersonal/?from=finance&tab=zx', callback=self.thx)
        # self.logger.info(response.body.decode('utf-8'))
        # for css in response.css('div.zxg-wrapper div#zxg-body div.zxg-stocklist'):
            # self.logger.info(css)
        # response.xpath('//*[@id="sh600703"]')

    def thx(self, response):
        self.logger.info(response.body)

#####################################################################################
