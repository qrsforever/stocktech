#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import scrapy
from crawlstocks.utils.common import zone_code

class CrawlLatestQuotationSpider(scrapy.Spider):
    name = 'sina.latestquota'
    debug = True

    allowed_domains = ['hq.sinajs.cn']

    custom_settings = {
            'ITEM_PIPELINES' : {
                # 'crawlstocks.pipelines.db.sina.LatestQuotaPipeline':100
                }
            }

    codes = list()

    def __init__(self, codesfile=None):
        if codesfile:
            with open(codesfile, 'r') as f:
                self.codes = [each.strip('\n') for each in f.readlines()]

    def start_requests(self):
        url0 = 'http://hq.sinajs.cn/list='
        p = 5
        symbols = []
        for i, each in enumerate(self.codes, 1):
            symbols.append(zone_code(each))
            if i % p == 0:
                yield scrapy.Request(url=url0+','.join(symbols))
                symbols = []
        else:
            yield scrapy.Request(url=url0+','.join(symbols))

    def parse(self, response):
        try:
            self.logger.info(response.url)
        except:
            self.logger.warn("parse error: %s", response.url)

    def closed(self, reason):
        self.logger.info(reason)

#####################################################################################
