#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy
import datetime
import re
from io import StringIO

from scrapy_splash import SplashRequest
from crawlstocks.items.tencent import TickDetailItem
from crawlstocks.utils.common import cookie_dict, zone_code, get_every_days

# TODO cookie not working, so with selenium work together.
class CrawlTickDetailSpider(scrapy.Spider):
    name = 'tencent.tickdetail'

    allowed_domains = [ 'gu.qq.com', 'stock.gtimg.cn' ]

    debug = False
    selenium = True

    custom_settings = {
            'REDIRECT_ENABLED': True,
            'COOKIES_ENABLED': True,
            # 去重过滤
            'DUPEFILTER_CLASS':'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
            'SPIDER_MIDDLEWARES': {
                'crawlstocks.middlewares.spider.CatchExceptionMiddleware': 600,
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
                },
            'DOWNLOADER_MIDDLEWARES': {
                'crawlstocks.middlewares.download.CatchExceptionMiddleware': 600,
                # 'crawlstocks.middlewares.download.DebugMiddleware': 820,
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
                },
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.tencent.TickDetailPipeline': 100,
                }
            }

    cookies = dict()
    codes = list()
    codesfile = list()

    url_prefix = 'http://stock.gtimg.cn/data/index.php'

    # attachment; filename="sh600532_成交明细_20190429.xls"
    re_fn = re.compile(r'attachment; filename="s[h|z](?P<code>[0369]\d{5})_.*_(?P<date>\d{8}).xls"')


    # 对请求的返回进行处理的配置
    meta = {
        # 'dont_merge_cookies': True, # 设置之后没cookies了
        # 'dont_redirect': True,  # 禁止网页重定向
        # 'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def __init__(self, cookiefile=None, codesfile=None):
        if cookiefile:
            self.cookies = cookie_dict(cookiefile)
        if codesfile:
            with open(codesfile, 'r') as f:
                self.codes = [each.strip('\n') for each in f.readlines()]

    def start_requests(self):
        if self.selenium:
            codes_last_date = dict()
            try:
                with open(self.settings.get('TICKDETAIL_LAST_DATE_FILE'), 'r') as f:
                    for line in f.readlines():
                        item = line.strip('\n').split(',')
                        codes_last_date[item[0]] = item[1]
            except Exception as e:
                self.logger.warn(e)

            end = datetime.datetime.now()
            begin = end + datetime.timedelta(days=-180)
            for code in self.codes:
                beg = begin
                try:
                    last = datetime.datetime.strptime(codes_last_date[code], '%Y%m%d')
                    if last and last > begin:
                        beg = last
                except:
                    pass
                for day in get_every_days(beg, end, flag = 1):
                    url = self.url_prefix + '?appn=detail&action=download&c={}&d={}'
                    yield scrapy.Request(url=url.format(zone_code(code), day))
                codes_last_date[code] = end.strftime('%Y%m%d')
                if self.debug: break
            with open(self.settings.get('TICKDETAIL_LAST_DATE_FILE'), 'w') as f:
                for key, value in codes_last_date.items():
                    f.write('{},{}\n'.format(key, value))
            return

        url = 'http://gu.qq.com/i'
        headers = {
                "Host": "gu.qq.com",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.7,zh-CN;q=0.3",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": 1,
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                }
        yield SplashRequest(url=url,
                method = 'GET',
                callback=self.parse_optionals,
                args={'wait': 8.0,'console': 1,'image': 1},
                headers=headers, cookies=self.cookies,
                meta=self.meta, dont_filter=True)

    def parse_optionals(self, response):
        # TODO cookie is not working
        self.logger.info('length = %d' % len(response.body.decode('utf8')))
        try:
            with open('/home/lidong/Downloads/cookie.html', 'w', encoding='utf-8') as f:
                s = response.body.decode()
                f.write(str(s))
        except Exception as e:
            self.logger.error(e)

        # parse codes

    def parse(self, response):
        self.logger.info('url: %s ' % response.url)
        item = TickDetailItem()
        try:
            res = self.re_fn.search(response.headers['Content-Disposition'].decode('gbk'))
            if res is None:
                return
            lines = StringIO(response.body.decode("gbk"))
            # the first line is header
            if len(lines.readline().split()) != 6:
                return
            code = res.groupdict()['code']
            date = res.groupdict()['date']
            while True:
                line = lines.readline()
                if line == '':
                    break;
                data = line.split()
                item['code'] = code
                item['datetime'] = datetime.datetime.strptime(date+data[0], '%Y%m%d%H:%M:%S')
                item['price'] = data[1]
                item['change'] = data[2]
                item['volume'] = data[3]
                item['amount'] = data[4]
                if data[5] == '买盘':
                    item['bstype'] = 'b'
                elif data[5] == '卖盘':
                    item['bstype'] = 's'
                else:
                    item['bstype'] = '-'
                item['_id'] = item['code'] + '_' + date + data[0].replace(':', '')
                yield item
                if self.debug: break
        except Exception as e:
            self.logger.error(e)

    def closed(self, reason):
        self.logger.info(reason)

#####################################################################################
