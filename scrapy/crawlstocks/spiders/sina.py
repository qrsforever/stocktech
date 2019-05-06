#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from io import StringIO
import time
import datetime
import scrapy

from crawlstocks.items.sina import LatestQuotaItem
from crawlstocks.utils.common import zone_code, is_stock_opening

class CrawlLatestQuotationSpider(scrapy.Spider):
    name = 'sina.latestquota'
    debug = True

    allowed_domains = ['hq.sinajs.cn']

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.net.sina.LatestQuotaPipeline':100
                }
            }

    re_data = re.compile(r'var hq_str_s[h|z](?P<code>[0369]\d{5})="(?P<data>[^"]*)".*')
    codes = list()

    def __init__(self, codesfile=None):
        if codesfile:
            with open(codesfile, 'r') as f:
                self.codes = [each.strip('\n') for each in f.readlines()]

    def start_requests(self):
        url0 = 'http://hq.sinajs.cn/list='
        while True:
            if not is_stock_opening():
                continue
            time.sleep(5)
            p = 10
            symbols = []
            for i, each in enumerate(self.codes, 1):
                symbols.append(zone_code(each))
                if i % p == 0:
                    yield scrapy.Request(url=url0+','.join(symbols), dont_filter=True)
                    symbols = []
            else:
                yield scrapy.Request(url=url0+','.join(symbols), dont_filter=True)

    def parse(self, response):
        self.logger.info(response.url)
        lines = StringIO(response.body.decode('gbk'))
        item = LatestQuotaItem()
        for line in lines:
            res = self.re_data.search(line)
            if res is None:
                continue
            code = res.groupdict()['code']
            data = res.groupdict()['data']
            values = data.split(',')
            if len(values) < 33:
                continue
            item['code'] = code
            item['name'] = values[0]
            item['curr_open'] = float(values[1])
            item['pre_close'] = float(values[2])
            item['price'] = float(values[3])
            item['high'] = float(values[4])
            item['low'] = float(values[5])
            item['bid'] = float(values[6])
            item['ask'] = float(values[7])
            item['volumn'] = float(values[8])
            item['amount'] = float(values[9])
            item['b1_v'] = float(values[10])
            item['b1_p'] = float(values[11])
            item['b2_v'] = float(values[12])
            item['b2_p'] = float(values[13])
            item['b3_v'] = float(values[14])
            item['b3_p'] = float(values[15])
            item['b4_v'] = float(values[16])
            item['b4_p'] = float(values[17])
            item['b5_v'] = float(values[18])
            item['b5_p'] = float(values[19])
            item['a1_v'] = float(values[20])
            item['a1_p'] = float(values[21])
            item['a2_v'] = float(values[22])
            item['a2_p'] = float(values[23])
            item['a3_v'] = float(values[24])
            item['a3_p'] = float(values[25])
            item['a4_v'] = float(values[26])
            item['a4_p'] = float(values[27])
            item['a5_v'] = float(values[28])
            item['a5_p'] = float(values[29])
            item['datetime'] = datetime.datetime.strptime(
                    values[30]+'_'+values[31], '%Y-%m-%d_%H:%M:%S')
            item['_id'] = code+'_' + values[30]+'_'+values[31]
            yield item

    def closed(self, reason):
        self.logger.info(reason)

#####################################################################################
