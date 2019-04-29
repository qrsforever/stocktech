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
    allowed_domains = ['stock.gtimg.cn']
    debug = False

    start_urls = ['http://gu.qq.com/i/']

    custom_settings = {
            'COOKIES_ENABLED': True,
            'DUPEFILTER_CLASS':'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
            'SPIDER_MIDDLEWARES': {
                'crawlstocks.middlewares.spider.CatchExceptionMiddleware': 600,
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
                },
            'DOWNLOADER_MIDDLEWARES': {
                'crawlstocks.middlewares.download.CatchExceptionMiddleware': 600,
               'scrapy_splash.SplashCookiesMiddleware': 723,
               'scrapy_splash.SplashMiddleware': 725,
               'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
                },
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.tencent.TickDetailPipeline': 100,
                }
            }

    def start_requests(self):
        # start_url = 'http://gu.qq.com/i/'
        start_url = 'http://gu.qq.com/i/#/1/all/mk'
        headers = {
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
                }
        cookies = trans_cookie('ptui_loginuin=985612771; RK=XerIrzpNdQ; ptcz=f3cfd6de3ef04bd730592c844754a8c9470c7e1eda23423f25abff50ae01d5e1; pgv_pvid=7204142455; pgv_pvi=9964695552; o_cookie=985612771; pac_uid=1_985612771; pgv_info=ssid=s535811180; sd_userid=41121556541101698; sd_cookie_crttime=1556541101698; ts_last=gu.qq.com/i/; ts_uid=2130993165; ptisp=cnc; pgv_si=s7207513088; check=10; appid=101481127; access_token=B09708DA55639DBB18C546ACDAEDA085; g_openid=255E578662AA421C6CFA1EACF97AFD9A; qq_openid=255E578662AA421C6CFA1EACF97AFD9A; refresh_token=F3A453E6F0B45EBF513E5A14C424DF33; headimgurl=http://thirdqq.qlogo.cn/g?b=oidb&k=FH3kRtbKyI9jSqE4HqAszA&s=100; loginString=check=10&appid=101481127&openid=255E578662AA421C6CFA1EACF97AFD9A&fskey=v0aaf8a82205cc6fb7fde0bccc61b1b9&access_token=B09708DA55639DBB18C546ACDAEDA085&g_openid=255E578662AA421C6CFA1EACF97AFD9A; openid=255E578662AA421C6CFA1EACF97AFD9A; fskey=v0aaf8a82205cc6fb7fde0bccc61b1b9; nickname=无敌东')
        print(cookies)
        yield SplashRequest(url=start_url,
                callback=self.parse,
                args={'wait': 9.0},
                headers=headers, cookies=cookies
                )
        # yield scrapy.Request(url=start_url,headers=headers, cookies=cookies)

    def parse(self, response):
        self.logger.info(response.body.decode('utf-8'))
        for css in response.css('div.zxg-wrapper div#zxg-body div.zxg-stocklist'):
            self.logger.info(css)
        # response.xpath('//*[@id="sh600703"]')


#####################################################################################
