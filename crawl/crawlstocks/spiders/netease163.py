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

    # def __init__(self, conf, *args, **kwargs):
    #     super(Quotesmoney163Spider, self).__init__(*args, **kwargs)
    #     self.conf = conf

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = cls(crawler.settings, *args, **kwargs)
    #     spider._set_crawler(crawler)
    #     return spider

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
        item = CHDDataItem()
        lines = StringIO(response.body.decode("gbk"))
        # the first line is header
        if len(lines.readline().split(',')) != 15:
            return
        while True:
            line = lines.readline()
            if line == '':
                break;
            data = line.strip().split(',')
            try:
                item['date'] = datetime.strptime(data[0], '%Y-%m-%d')
                item['code'] = data[1][1:]
                item['name'] = data[2]
                item['tclose'] = float(data[3])
                item['high'] = float(data[4])
                item['low'] = float(data[5])
                item['topen'] = float(data[6])
                item['lclose'] = float(data[7])
                item['chg'] = float(data[8])
                item['pchg'] = float(data[9])
                item['turnover'] = float(data[10])
                item['voturnover'] = float(data[11])
                item['vaturnover'] = float(data[12])
                item['tcap'] = float(data[13])
                item['mcap'] = float(data[14])
                item['_id'] = item['code'] + '_' + data[0]
                yield item
                if self.debug:
                    break
            except:
                self.logger.warn("parse error: %s", line)

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
        

