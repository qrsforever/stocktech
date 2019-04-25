# -*- coding: utf-8 -*-
import re
import scrapy

from crawlstocks.items import GuchengStockCodeItem

class GuchengblockcodesSpider(scrapy.Spider):
    name = 'GuchengBlockCodes'
    allowed_domains = ['hq.gucheng.com']

    custom_settings = {
            'ITEM_PIPELINES' : {'crawlstocks.pipelines.file.GuchengCrawlListPipeline':200}
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
        item = GuchengStockCodeItem()
        for css in response.css('tbody tr td.stock_phone.stock_textLeft a'):
            item['name'] = re.sub(r'\s+', '', css.xpath('./text()').get())
            item['code'] = css.xpath('./@href').get()[1:-1]
            yield item
        # not work
        # next = response.css('div.stock_page span a[text*="下一页"]::text').get()
        #  /html/body/article/div/div[4]/section/div/span[8]/a
        next_page = response.xpath('//div[contains(@class, \
                "stock_page")]/span/a[contains(.//text(), "下一页")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
