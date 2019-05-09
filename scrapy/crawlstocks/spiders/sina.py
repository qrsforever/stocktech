#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from io import StringIO
import time
import datetime
import scrapy

from crawlstocks.items.sina import LatestQuotaItem
from crawlstocks.utils.common import code_to_symbol, is_stock_opening

class CrawlLatestQuotationSpider(scrapy.Spider):
    name = 'sina.latestquota'
    debug = False

    allowed_domains = ['hq.sinajs.cn']

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.sina.LatestQuotaPipeline':200,
                'crawlstocks.pipelines.net.sina.LatestQuotaPipeline':300,
                'crawlstocks.pipelines.file.sina.LatestQuotaPipeline':500,
                }
            }

    re_data = re.compile(r'var hq_str_s[h|z](?P<code>[0369]\d{5})="(?P<data>[^"]*)".*')

    def __init__(self, codesfile=None):
        self.codesfile = codesfile

    def start_requests(self):
        url0 = 'http://hq.sinajs.cn/list='
        codes = list()
        if self.codesfile:
            with open(self.codesfile, 'r') as f:
                codes = [each.strip('\n') for each in f.readlines()]
        else:
            with open(self.settings.get('STOCK_OPTIONALS_FILE'), 'r') as f:
                codes = [each.strip('\n') for each in f.readlines()]
        while True:
            if not self.debug:
                if datetime.datetime.now().hour >= 15:
                    return
                time.sleep(3)
                if not is_stock_opening():
                    time.sleep(10)
                    continue
            p = 10
            symbols = []
            for i, each in enumerate(codes, 1):
                symbols.append(code_to_symbol(each))
                if i % p == 0:
                    yield scrapy.Request(url=url0+','.join(symbols), dont_filter=True)
                    symbols = []
            else:
                yield scrapy.Request(url=url0+','.join(symbols), dont_filter=True)
            if self.debug: return

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
            item['open'] = float(values[1])
            item['settlement'] = float(values[2])
            if item['open'] == 0.0 or item['settlement'] == 0.0:
                return
            item['price'] = float(values[3])
            item['high'] = float(values[4])
            item['low'] = float(values[5])
            item['b_p'] = float(values[6])
            item['a_p'] = float(values[7])
            item['volume'] = int(int(values[8])/100)
            item['amount'] = int(float(values[9])/10000)
            item['b1_v'] = int(int(values[10])/100)
            item['b1_p'] = float(values[11])
            item['b2_v'] = int(int(values[12])/100)
            item['b2_p'] = float(values[13])
            item['b3_v'] = int(int(values[14])/100)
            item['b3_p'] = float(values[15])
            item['b4_v'] = int(int(values[16])/100)
            item['b4_p'] = float(values[17])
            item['b5_v'] = int(int(values[18])/100)
            item['b5_p'] = float(values[19])
            item['a1_v'] = int(int(values[20])/100)
            item['a1_p'] = float(values[21])
            item['a2_v'] = int(int(values[22])/100)
            item['a2_p'] = float(values[23])
            item['a3_v'] = int(int(values[24])/100)
            item['a3_p'] = float(values[25])
            item['a4_v'] = int(int(values[26])/100)
            item['a4_p'] = float(values[27])
            item['a5_v'] = int(int(values[28])/100)
            item['a5_p'] = float(values[29])
            item['datetime'] = datetime.datetime.strptime(
                    values[30]+'_'+values[31], '%Y-%m-%d_%H:%M:%S')
            item['_id'] = code+'_' + values[30]+'_'+values[31]
            yield item
            if self.debug: return

    def closed(self, reason):
        self.logger.info(reason)

#####################################################################################
