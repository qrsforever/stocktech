# -*- coding: utf-8 -*-
import os
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawlstocks.items import GuchengStockInfoItem

class GuchengstockinfoSpider(CrawlSpider):
    name = 'GuchengStockInfo'
    allowed_domains = ['hq.gucheng.com']
    start_urls = ['https://hq.gucheng.com/gpdmylb.html']

    custom_settings = {
            'ITEM_PIPELINES' : {'crawlstocks.pipelines.file.GuchengCrawlInfoPipeline':200}
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
        # 链接追加财务分析项, 注意最后的"/"符号, 避免redirect
        #  for link in links:
        #    link.url = os.path.join(link.url, "caiwufenxi/")
        #  return links
        for link in links:
            if '国债' in link.text:
                continue
            if '基金' in link.text:
                continue
            if '指数' in link.text:
                continue
            link.url = os.path.join(link.url, "caiwufenxi/")
            yield link


    def parse_item(self, response):
        # self.logger.info(response.url)
        item = GuchengStockInfoItem()
        # 股票名字
        item['name'] = re.sub(r'\s+', '', response.xpath('//header/h1/text()').get())
        # 股票代码
        item['code'] = response.xpath('//header/h2/text()').get()
        selector = response.xpath('//section[@class="stock_company stock_f10 cwzyzb"]/div/table[1]/tbody')
        # 报告期
        item['report_date'] = selector.xpath('./tr[1]/td[2]/div/text()').get()
        # 每股收益（元）
        item['earning_ps'] = selector.xpath('./tr[2]/td[3]/div/text()').get()
        # 每股净资产（元）
        item['net_assets_ps'] = selector.xpath('./tr[3]/td[2]/div/text()').get()
        # 净利润（亿元）
        item['net_profit'] = selector.xpath('./tr[2]/td[6]/div/text()').get()
        # 净资产（亿元）
        item['net_asset'] = selector.xpath('./tr[7]/td[2]/div/text()').get()
        # 营业收入（亿元）
        item['gross_sales'] = selector.xpath('./tr[7]/td[5]/div/text()').get()
        # 净资产收益率（%）
        item['ROE'] = selector.xpath('./tr[4]/td[2]/div/text()').get()
        # 市盈率
        item['PER'] = selector.xpath('./tr[6]/td[3]/div/text()').get()
        # 市净率
        item['PBR'] = selector.xpath('./tr[4]/td[5]/div/text()').get()
        # 每股现金流净额（元）
        item['cash_flow_ps'] = selector.xpath('./tr[5]/td[4]/div/text()').get()
        # 销售毛利率（%）
        item['gross_profit'] = selector.xpath('./tr[3]/td[4]/div/text()').get()
        yield item
