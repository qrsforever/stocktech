#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime
from io import StringIO
from crawlstocks.items.netease163 import CHDDataItem
from pymongo import MongoClient

class CrawlChdDataSpider(scrapy.Spider):
    name = 'netease163.chddata'
    allowed_domains = ['quotes.money.163.com']

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
    URL = 'http://xquotes.money.163.com/service/chddatb.html?'

    def start_requests(self):
        # mongo = MongoClient(self.conf.get('DB_HOST'))
        mongo = MongoClient(self.settings.get('DB_HOST'))
        db = mongo[self.settings.get('DB_NAME')]
        table = db[self.settings.get('DB_CODES_TABLE_NAME')]
        for each in table.find({}, {'_id':0, 'code':1}):
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
            yield scrapy.Request(link, callback=self.parse_csv)
            # 调试
            break
        mongo.close()

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
                break
            except:
                self.logger.warn("parse error: %s", line)

    def closed(self, reason):
        self.logger.info(reason)
