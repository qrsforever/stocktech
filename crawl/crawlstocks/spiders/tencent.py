#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy
from io import StringIO
from datetime import datetime
from pymongo import MongoClient

from crawlstocks.items.netease163 import CHDDataItem
from crawlstocks.exceptions import DownloadException
from crawlstocks.items.items import CrawlErrorItem

class CrawlChdDataSpider(scrapy.Spider):
    name = 'netease163.chddata'
    allowed_domains = ['quotes.money.163.com']
    debug = True

    custom_settings = {
            'SPIDER_MIDDLEWARES': {
                'crawlstocks.middlewares.spider.CatchExceptionMiddleware': 600,
                },
            'DOWNLOADER_MIDDLEWARES': {
                'crawlstocks.middlewares.download.CatchExceptionMiddleware': 600,
                },
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.netease163.CHDDataPipeline': 100,
                }
            }


    FIELDS = "TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
    URL = 'http://quotes.money.163.com/service/chddatb.html?'

    def start_requests(self):
        self.client = MongoClient(self.settings.get('DB_URI',
            'mongodb://localhost:27017/'))
        db = self.client[self.settings.get('DB_NAME', 'stocktech')]
        self.err_col = db[self.settings.get('DB_ERRORS_COLLECTION_NAME', 'errors')]

        col = db[self.settings.get('DB_CODES_COLLECTION_NAME', 'codes')]
        for each in col.find({}, {'_id':0, 'code':1}):
            code = each['code']
            if code[0] == '6':
                code = '0' + code
            else:
                code = '1' + code
            link = self.URL + 'code={0}&start={1}&end={2}&fields={3}'.format(
                    code,
                    self.settings.get('DATETIME_START'),
                    self.settings.get('DATETIME_END'),
                    self.FIELDS)
            yield scrapy.Request(link, callback=self.parse_csv, errback=self.err_back)
            if self.debug:
                break

    def parse_csv(self, response):

    def err_back(self, failure):
        if failure.check(DownloadException):
            if self.err_col is not None:
                item = CrawlErrorItem()
                item['url'] = failure.request.url
                item['tag'] = 'DownloadException'
                item['message'] = failure.getErrorMessage()
                item['errtime'] = datetime.now()
                item['_id'] = item['url']
                self.err_col.update_one({'_id': item['_id']},
                    {'$set': dict(item)}, upsert = True)
                self.logger.error('DownloadException on %s', item)
        else:
            self.logger.error(repr(failure))

    def closed(self, reason):
        self.logger.info(reason)
        self.client.close()


#####################################################################################
        

