#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file xinhuanet.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-17 19:50:21

import scrapy
from scrapy.spiders import Spider
import datetime, time
import os

from crawlstocks.items.xinhuanet import LeaderNewsItem
from crawlstocks.utils.common import is_stock_opening

class CrawlLeaderNewsSpider(Spider):
    name = 'xinhuanet.leardernews'
    allowed_domains = ['www.xinhuanet.com']

    debug = False

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.xinhuanet.LeaderNewsPipeline':200,
                'crawlstocks.pipelines.net.xinhuanet.LeaderNewsPipeline':200
                }
            }

    # 防止重复解析/操作DB
    url_cache = {}
    today = None

    def __init__(self, force=False, debug=None):
        self.force = force
        if debug:
            self.debug = debug
        today = datetime.datetime.now().strftime('%Y%m%d')
        self.today = datetime.datetime.strptime(today, '%Y%m%d')

    def start_requests(self):
        url0 = 'http://www.xinhuanet.com/politics/leaders/xijinping/'
        tmpdir = os.path.join(self.settings.get('TMP_DIR'), self.name)
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        date = datetime.datetime.now().strftime('%Y%m%d')
        self.filepath = os.path.join(tmpdir, date + '.txt')
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    for url in f.readlines():
                        self.url_cache[url.strip()] = True
        except Exception as e:
            self.logger.info("open error:", e)
        while True:
            if not self.debug:
                now = datetime.datetime.now().hour
                if (now >= 15 or now <= 8) and not self.force:
                    sleep_interval = 3600
                else:
                    if not is_stock_opening():
                        sleep_interval = 300
                    else:
                        sleep_interval = 20
            else:
                sleep_interval = 1
            for page in ['pszs', 'zdzxa', 'kcsc', 'hyhd']:
                yield scrapy.Request(url=url0 + page + ".htm",
                        callback=self.parse_item,
                        dont_filter=True)
            time.sleep(sleep_interval)
            if self.debug: return

    def parse_item(self, response):
        try:
            if not self.debug:
                datestr = response.css('ul.xpage-content-list li::attr(data-pt)').get()
                dateobj = datetime.datetime.strptime(datestr.strip(), '%Y-%m-%d')
                if dateobj < self.today:
                    return
            link = response.css('ul.xpage-content-list li a::attr(href)').get()
            if self.url_cache.get(link.strip(), None):
                return
            else:
                tag = response.css('div.box div.blocks-tit a::text').get()
                yield scrapy.Request(link, meta={'tag': tag},
                        callback=self.parse_news)
        except Exception as e:
            self.logger.warn(e)

    def parse_news(self, response):
        self.logger.info(response.url)
        item = LeaderNewsItem()
        try:
            # 取第一个消息即可
            item['title'] = response.css('div.h-title::text').get().strip()
            item['datetime'] = response.css('span.h-time::text').get().strip()
            item['html'] = response.body.decode("utf-8")
            item['tag'] = response.meta['tag']
            item['url'] = response.url
            yield item
            with open(self.filepath, 'a') as f:
                f.write("%s\n" % response.url)
            self.url_cache[response.url] = True
        except Exception as e:
            self.logger.warn(e)

#####################################################################################
