# -*- coding: utf-8 -*-
import scrapy
import re

from crawlstocks.items import EastmoneyStockUrlItem

class EastmoneystockurlsSpider(scrapy.Spider):
    name = 'EastmoneyStockUrls'
    allowed_domains = [
            #  'quote.eastmoney.com',
            #  'f9.eastmoney.com',
            'hq.gucheng.com',
            ]
    start_urls = [
            #  'http://quote.eastmoney.com/stocklist.html',
            'https://hq.gucheng.com/gpdmylb.html',
            ]
    custom_settings = {
            'ITEM_PIPELINES' : {'crawlstocks.pipelines.file.EastmoneyCrawlUrlsPipeline':200}
            }

    def parse(self, response):
        re_code = re.compile(r'(.+)\((?P<code>[0369]\d{5})\)')
        item = EastmoneyStockUrlItem()
        for stock in response.xpath('//section[has-class("stockTable")]/a/text()').getall():
            res = re_code.search(stock)
            if res is None:
                continue
            # 股票代码
            code = res.groupdict()['code']
            addr = "sz"
            if code[0] == '6':
                addr = "sh"
            item['stock_url'] = 'http://quote.eastmoney.com/' + addr + code + ".html"
            yield item
