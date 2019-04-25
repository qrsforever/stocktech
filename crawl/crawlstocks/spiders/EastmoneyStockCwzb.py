# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from crawlstocks.items import EastmoneyStockCwzbItem

# 平安银行(000001.SZ)深度F9-PC_HSF9资料
re_name_code = re.compile(r'(?P<name>.+)\((?P<code>[0369]\d{5})\.*\)*')
re_replace_f9 = re.compile('quote')

class EastmoneystockcwzbSpider(scrapy.Spider):
    name = 'EastmoneyStockCwzb'
    allowed_domains = [
            'quote.eastmoney.com',
            'f9.eastmoney.com',
            ]
    custom_settings = {
            'ITEM_PIPELINES': {
                'crawlstocks.pipelines.file.EastmoneyCrawlCwzbPipeline':200,
                },
            'SPLASH_URL': 'http://localhost:8050',
            'DOWNLOADER_MIDDLEWARES': {
               'crawlstocks.middlewares.CustomRandomMiddleware.RandomUserAgentMiddleware': 543,
               'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
               'scrapy_splash.SplashCookiesMiddleware': 723,
               'scrapy_splash.SplashMiddleware': 725,
               'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
               },
            'SPIDER_MIDDLEWARES': {
               'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
               },
            'DUPEFILTER_CLASS':'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
            }
    # 调试
    start_urls = ['http://quote.eastmoney.com/sh600751.html']

    def __init__(self, filename=None):
        if filename:
           try:
               with open(filename, 'r', encoding='utf-8') as f:
                   # map的返回是个生成器, 效率高很多, 在引擎中访问start_urls的时候才触发真正数据
                   self.start_urls = map(lambda line: line.strip('\n'), f.readlines())
           except:
               self.logger.info("open file:%s error!" % filename)

    # 1. http://quote.eastmoney.com/sz000056.html
    # 2. <a href="http://f9.eastmoney.com/sz000056.html#cwzb" target="_blank">财务指标</a>
    # 3. http://f9.eastmoney.com/sz000056.html#cwzb
    # 提取财务指标的URL (页面是动态异步加载, 直接请求可能拿不到tbody, 所以使用
    # SplashRequest传递一个等待页面加载时间, cwzb页面加载太慢了....
    # wait time must < splash --max-timeout
    def start_requests(self):
        for url in self.start_urls:
            # 自行解析财务指标中的link
            # yield SplashRequest(url,
            #        callback=self.parse_link,
            #        args={'wait': 2.0},
            #        )
            
            # 直接拼接出, 缺点是如果地址变更就失效, 但是效率高了一倍
            # link = url.replace("quote", "f9") + '#cwzb'
            link = re_replace_f9.sub('f9', url) + '#cwzb'
            self.logger.info("link: %s" % link)
            yield SplashRequest(link,
                  callback=self.parse_cwzb,
                  args={'wait': 9.0},
                  )

    # def parse_link(self, response):
    #     link = response.xpath('//a[contains(@href, "cwzb")]/@href').get()
    #     self.logger.info("link: %s" % link)
    #     yield SplashRequest(link,
    #            callback=self.parse_cwzb,
    #            args={'wait': 4.0},
    #            )
    #    #  yield scrapy.Request(link, callback=self.parse_cwzb)

    # 解析财务指标数据
    def parse_cwzb(self, response):
        #  self.logger.info(response.url)
        res = re_name_code.search(response.xpath('//title/text()').get())
        if res is None:
            return
        item = EastmoneyStockCwzbItem()
        item['name'] = re.sub(r'\s+', '', res.groupdict()['name'])
        item['code'] = res.groupdict()['code']
        body = response.xpath('//*[@id="zyzb_content"]/table/tbody')
        if len(body) == 0:
            self.logger.warn("tbody is null")
            return
        item['report_date'] = body.xpath('./tr[1]/td[2]/text()').get()             # 截止日期
        item['eps'] = body.xpath('./tr[2]/td[2]/text()').get()                     # 每股收益(元): EPS
        item['deducted_eps'] = body.xpath('./tr[3]/td[2]/text()').get()            # 扣非每股收益(元)
        item['diluted_eps'] = body.xpath('./tr[4]/td[2]/text()').get()             # 稀释每股收益(元)
        item['net_profit'] = body.xpath('./tr[5]/td[2]/text()').get()              # 净利润(亿元）
        item['net_profit_yony'] = body.xpath('./tr[6]/td[2]/text()').get()         # 净利润同比增长(%)
        item['net_profit_monm'] = body.xpath('./tr[7]/td[2]/text()').get()         # 净利润滚动环比增长(%)
        item['ROE_WA'] = body.xpath('./tr[8]/td[2]/text()').get()                  # 加权净资产收益率(%）
        item['ROE_ED'] = body.xpath('./tr[9]/td[2]/text()').get()                  # 摊薄净资产收益率(%)
        item['gross_profit'] = body.xpath('./tr[10]/td[2]/text()').get()           # 毛利率(%）
        item['eff_tax_rate'] = body.xpath('./tr[11]/td[2]/text()').get()           # 实际税率(%)
        item['deposit_gross_rate'] = body.xpath('./tr[12]/td[2]/text()').get()     # 预收款/营业收入
        item['cashflow_gross_rate'] = body.xpath('./tr[13]/td[2]/text()').get()    # 销售现金流/营业收入
        item['total_assets_turnover'] = body.xpath('./tr[14]/td[2]/text()').get()  # 总资产周转率(次)
        item['liability_assets_rate'] = body.xpath('./tr[15]/td[2]/text()').get()  # 资产负债率(%)
        item['debt_flow_total_rate'] = body.xpath('./tr[16]/td[2]/text()').get()   # 流动负债/总负债(%)
        yield item
