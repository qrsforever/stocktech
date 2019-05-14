#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file gucheng.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-09 14:47:19


import os
import re
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawlstocks.items.gucheng import StockCodeItem
from crawlstocks.items.gucheng import FinancialInfoItem

class CrawlStockCodeSpider(scrapy.Spider):
    name = 'gucheng.stockcode'
    debug = False

    allowed_domains = ['hq.gucheng.com']
    start_urls = ['https://hq.gucheng.com/gpdmylb.html']

    re_name_code = re.compile(r'(?P<name>.+)\((?P<code>[0369]\d{5})\)')


    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.file.gucheng.StockCodePipeline':200,
                'crawlstocks.pipelines.db.gucheng.StockCodePipeline':100
                }
            }

    def parse(self, response):
        item = StockCodeItem()
        try:
            for stock in response.xpath('//section[has-class("stockTable")]/a/text()').getall():
                res = self.re_name_code.search(stock)
                if res is None:
                    continue
                # 股票名称 并去除名字中空格
                item['name'] = re.sub(r'\s+', '', res.groupdict()['name'])
                item['code'] = res.groupdict()['code']
                yield item
                if self.debug: break
        except:
            self.logger.warn("parse error: %s", response.url)


#####################################################################################


class CrawlFinancialInfoSpider(CrawlSpider):
    name = 'gucheng.financialinfo'
    debug = False

    allowed_domains = ['hq.gucheng.com']
    start_urls = ['https://hq.gucheng.com/gpdmylb.html']

    custom_settings = {
            'ITEM_PIPELINES' : {'crawlstocks.pipelines.file.gucheng.FinancialInfoPipeline':200}
            }

    # 提取需要请求的链接 (SZ SH)
    rules = (
        Rule(LinkExtractor(
            allow=('hq.gucheng.com/[sS][hzHZ][036]\d{5}/'),
            restrict_xpaths=('//section[@class="stockTable"]'),
            ),
            callback='parse_item',
            process_links='deal_links',
            process_request='deal_request',
            follow=True),
    )

    def deal_request(self, request):
        # 禁止重定向
        request.meta['dont_redirect'] = True
        return request

    def deal_links(self, links):
        count = 0
        total = len(links)
        for link in links:
            if '国债' in link.text:
                continue
            if '基金' in link.text:
                continue
            if '指数' in link.text:
                continue
            # 链接追加财务分析项, 注意最后的"/"符号, 避免redirect
            link.url = os.path.join(link.url, "caiwufenxi/")
            self.logger.info("[%.2f] : %s" % (count * 100 / total, link.url))
            count += 1
            yield link
            if self.debug: break

    def parse_item(self, response):
        item = FinancialInfoItem()
        try:
            item['name'] = re.sub(r'\s+', '', response.xpath('//header/h1/text()').get())
            item['code'] = response.xpath('//header/h2/text()').get()
            selector = response.xpath('//section[@class="stock_company stock_f10 cwzyzb"]/div/table[1]/tbody')
            item['report_date'] = selector.xpath('./tr[1]/td[2]/div/text()').get()
            item['earning_ps'] = selector.xpath('./tr[2]/td[3]/div/text()').get()
            item['net_assets_ps'] = selector.xpath('./tr[3]/td[2]/div/text()').get()
            item['net_profit'] = selector.xpath('./tr[2]/td[6]/div/text()').get()
            item['net_asset'] = selector.xpath('./tr[7]/td[2]/div/text()').get()
            item['gross_sales'] = selector.xpath('./tr[7]/td[5]/div/text()').get()
            item['ROE'] = selector.xpath('./tr[4]/td[2]/div/text()').get()
            item['PER'] = selector.xpath('./tr[6]/td[3]/div/text()').get()
            item['PBR'] = selector.xpath('./tr[4]/td[5]/div/text()').get()
            item['cash_flow_ps'] = selector.xpath('./tr[5]/td[4]/div/text()').get()
            item['gross_profit'] = selector.xpath('./tr[3]/td[4]/div/text()').get()
            yield item
        except:
            self.logger.warn("parse error: %s", response.url)


#####################################################################################


class CrawlBlockCodeSpider(scrapy.Spider):
    name = 'gucheng.blockcode'
    allowed_domains = ['hq.gucheng.com']

    custom_settings = {
            'ITEM_PIPELINES' : {'crawlstocks.pipelines.file.gucheng.StockCodePipeline':200}
            }

    def __init__(self, blockname='xiongan'):
        if blockname == 'xiongan':
            blid = '003813'        # 雄安新区
        elif blockname == 'jingjinyi':
            blid = '003684'        # 京津翼一体化
        else:
            blid = '003813'        # 雄安新区

        self.start_urls = ['https://hq.gucheng.com/blockInfo/' + blid + '/']

    def parse(self, response):
        # self.logger.info(response.url)
        #  <td class="stock_phone stock_textLeft"><a href="/SZ300353/" target="_blank">东土科技</a></td>
        item = StockCodeItem()
        for css in response.css('tbody tr td.stock_phone.stock_textLeft a'):
            item['name'] = re.sub(r'\s+', '', css.xpath('./text()').get())
            item['code'] = css.xpath('./@href').get()[1:-1]
            yield item
        # not work below
        # next = response.css('div.stock_page span a[text*="下一页"]::text').get()
        #  /html/body/article/div/div[4]/section/div/span[8]/a
        next_page = response.xpath('//div[contains(@class, \
                "stock_page")]/span/a[contains(.//text(), "下一页")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

