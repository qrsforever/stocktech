#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-07 15:31:37

import scrapy
import demjson
import datetime, time
import re
from io import StringIO

from scrapy_splash import SplashRequest
from crawlstocks.items.tencent import StockCodeItem
from crawlstocks.items.tencent import TapeReadingItem
from crawlstocks.items.tencent import TickDetailItem
from crawlstocks.items.tencent import RealtimeQuotaItem
from crawlstocks.items.tencent import CashFlowItem

from crawlstocks.utils.common import cookie_dict, code_to_symbol
from crawlstocks.utils.common import get_every_days, is_stock_opening

class CrawlStockCodeSpider(scrapy.Spider):
    name = 'tencent.stockcode'
    allowed_domains = [ 'stock.gtimg.cn' ]
    debug = False

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.file.tencent.StockCodePipeline':100,
                }
            }
    url = 'http://stock.gtimg.cn/data/index.php?appn=rank&' \
            't=rank{}/code&p={}&o=0&l=100&v=list_data'

    def __init__(self, cat='a'):
        self.category = cat # 'a, b, ash, asz, bsh, bsz'

    def start_requests(self):
        yield scrapy.Request(self.url.format(self.category, 1), dont_filter=True)

    def parse(self, response):
        self.logger.info(response.url)
        jdata = demjson.decode(response.body[len('var list_data='): -1])
        if not jdata:
            return
        item = StockCodeItem()
        for code in jdata['data'].split(','):
            item['code'] = code[2:]
            yield item
        total = int(jdata['total'])
        ipage = int(jdata['p'])
        if ipage < total:
            yield scrapy.Request(self.url.format(self.category, ipage+1),
                    dont_filter=True)


#####################################################################################


# TODO cookie not working, so with selenium work together.
class CrawlTickDetailSpider(scrapy.Spider):
    name = 'tencent.tickdetail'

    allowed_domains = [ 'gu.qq.com', 'stock.gtimg.cn' ]

    debug = True
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
    codes_last_date = dict()

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
        self.codesfile = codesfile

    def start_requests(self):
        if self.selenium:
            codes = list()
            if self.codesfile:
                with open(self.codesfile, 'r') as f:
                    codes = [each.strip('\n') for each in f.readlines()]
            else:
                with open(self.settings.get('STOCK_OPTIONALS_FILE'), 'r') as f:
                    codes = [each.strip('\n') for each in f.readlines()]
            try:
                with open(self.settings.get('TICKDETAIL_LAST_DATE_FILE'), 'r') as f:
                    for line in f.readlines():
                        item = line.strip('\n').split(',')
                        self.codes_last_date[item[0]] = item[1]
            except Exception as e:
                self.logger.warn(e)

            end = datetime.datetime.now()
            begin = end + datetime.timedelta(days=-180)
            for code in codes:
                beg = begin
                try:
                    last = datetime.datetime.strptime(self.codes_last_date[code], '%Y%m%d')
                    if last and last > begin:
                        beg = last
                except:
                    pass
                for day in get_every_days(beg, end, flag = 1):
                    url = self.url_prefix + '?appn=detail&action=download&c={}&d={}'
                    yield scrapy.Request(url=url.format(code_to_symbol(code), day))
                self.codes_last_date[code] = end.strftime('%Y%m%d')
                if self.debug: break
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
                    item['bstype'] = 'B'
                elif data[5] == '卖盘':
                    item['bstype'] = 'S'
                else:
                    item['bstype'] = 'M'
                item['_id'] = item['code'] + '_' + date + data[0].replace(':', '')
                yield item
                if self.debug: break
        except Exception as e:
            self.logger.error(e)

    def closed(self, reason):
        self.logger.info(reason)
        with open(self.settings.get('TICKDETAIL_LAST_DATE_FILE'), 'w') as f:
            for key, value in self.codes_last_date.items():
                f.write('{},{}\n'.format(key, value))


#####################################################################################


class CrawlRealtimeQuotaSpider(scrapy.Spider):
    name = 'tencent.realtimequota'

    allowed_domains = [ 'qt.gtimg.cn' ]

    debug = False

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.tencent.RealtimeQuotaPipeline':100,
                'crawlstocks.pipelines.net.tencent.RealtimeQuotaPipeline':200
                }
            }

    re_data = re.compile(r'v_s[h|z][0369]\d{5}="(?P<data>[^"]*)".*')

    def __init__(self, codesfile=None):
        self.codesfile = codesfile

    def start_requests(self):
        url0 = 'http://qt.gtimg.cn/q='
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
            for each in codes:
                yield scrapy.Request(url=url0+code_to_symbol(each), dont_filter=True)
            if self.debug: return

    def parse(self, response):
        # self.logger.info(response.url)
        result = response.body.decode('gbk')
        res = self.re_data.search(result)
        if res is None:
            return
        data = res.groupdict()['data']
        values = data.split('~')
        if len(values) < 49:
            return
        item = RealtimeQuotaItem()
        item['name'] = values[1]
        item['code'] = values[2]
        item['price'] = float(values[3])
        item['settlement'] = float(values[4])
        item['open'] = float(values[5])
        item['volume'] = int(int(values[6])/100)
        item['b_v'] = float(values[7])
        item['a_v'] = float(values[8])
        item['b1_p'] = float(values[9])
        item['b1_v'] = int(int(values[10])/100)
        item['b2_p'] = float(values[11])
        item['b2_v'] = int(int(values[12])/100)
        item['b3_p'] = float(values[13])
        item['b3_v'] = int(int(values[14])/100)
        item['b4_p'] = float(values[15])
        item['b4_v'] = int(int(values[16])/100)
        item['b5_p'] = float(values[17])
        item['b5_v'] = int(int(values[18])/100)
        item['a1_p'] = float(values[19])
        item['a1_v'] = int(int(values[20])/100)
        item['a2_p'] = float(values[21])
        item['a2_v'] = int(int(values[22])/100)
        item['a3_p'] = float(values[23])
        item['a3_v'] = int(int(values[24])/100)
        item['a4_p'] = float(values[25])
        item['a4_v'] = int(int(values[26])/100)
        item['a5_p'] = float(values[27])
        item['a5_v'] = int(int(values[28])/100)
        item['recent_trades'] = values[29]
        item['datetime'] = datetime.datetime.strptime(values[30], '%Y%m%d%H%M%S')
        item['chg'] = float(values[31])
        item['pchg'] = float(values[32])
        item['high'] = float(values[33])
        item['low'] = float(values[34])
        item['price_volume_amount'] = values[35]
        item['volume'] = int(int(values[36])/100)
        item['amount'] = float(values[37])
        item['turnover'] = float(values[38])
        item['PE'] = float(values[39])
        item['unknown'] = values[40]
        item['high2'] = float(values[41])
        item['low2'] = float(values[42])
        item['amplitude'] = float(values[43])
        item['mcap'] = float(values[44])
        item['tcap'] = float(values[45])
        item['PB'] = float(values[46])
        item['topest'] = float(values[47])
        item['lowest'] = float(values[48])
        item['_id'] = item['code'] + '_' + values[30]
        yield item
        if self.debug: return

    def closed(self, reason):
        self.logger.info(reason)


#####################################################################################


class CrawlCashFlowSpider(scrapy.Spider):
    name = 'tencent.cashflow'

    allowed_domains = [ 'qt.gtimg.cn' ]

    debug = False

    custom_settings = {
            'ITEM_PIPELINES' : {
                'crawlstocks.pipelines.db.tencent.CashFlowPipeline':100,
                'crawlstocks.pipelines.net.tencent.CashFlowPipeline':200
                }
            }

    re_data = re.compile(r'v_ff_s[h|z](?P<code>[0369]\d{5})="(?P<data>[^"]*)".*')

    def __init__(self, codesfile=None):
        self.codesfile = codesfile

    def start_requests(self):
        url0 = 'http://qt.gtimg.cn/q=ff_{symbol}'
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
            for each in codes:
                yield scrapy.Request(url=url0.format(code_to_symbol(each)),
                        dont_filter=True)
            if self.debug: return

    def parse(self, response):
        # self.logger.info(response.url)
        result = response.body.decode('gbk')
        res = self.re_data.search(result)
        if res is None:
            return
        data = res.groupdict()['data']
        code = res.groupdict()['code']
        values = data.split('~')
        if len(values) < 21:
            return
        item = CashFlowItem()
        item['code']          = code
        item['main_in']       = float(values[1])
        item['main_out']      = float(values[2])
        item['main_net']      = float(values[3])
        item['main_net_rate'] = float(values[4])
        item['priv_in']       = float(values[5])
        item['priv_out']      = float(values[6])
        item['priv_net']      = float(values[7])
        item['priv_net_rate'] = float(values[8])
        item['total_cash']    = float(values[9])
        item['unkown1']       = values[10]
        item['unkown2']       = values[11]
        item['name']          = values[12]
        item['date']          = values[13]
        item['before_day1']   = values[14]
        item['before_day2']   = values[15]
        item['before_day3']   = values[16]
        item['before_day4']   = values[17]
        item['unkown3']       = values[18]
        item['unkown4']       = values[19]
        item['datetime']      = datetime.datetime.strptime(values[20], '%Y%m%d%H%M%S')
        item['_id']           = code + '_' + values[20]
        yield item
        if self.debug: return

    def closed(self, reason):
        self.logger.info(reason)


#####################################################################################

class CrawlTapeReadingSpider(scrapy.Spider):
    name = 'tencent.tapereading'

    allowed_domains = [ 'qt.gtimg.cn' ]

    debug = True

    custom_settings = {
            'DOWNLOAD_DELAY': 0.5,
            'CONCURRENT_REQUESTS': 8,
            'ITEM_PIPELINES': {
                # 'crawlstocks.pipelines.db.tencent.TapeReadingPipeline':100,
                'crawlstocks.pipelines.net.tencent.TapeReadingPipeline':200
                }
            }

    re_handicap = re.compile(r'v_s_pks[h|z](?P<code>[0369]\d{5})="(?P<data>[^"]*)".*')
    re_brief = re.compile(r'v_s_s[h|z](?P<code>[0369]\d{5})="(?P<data>[^"]*)".*')

    def __init__(self, codesfile=None):
        self.codesfile = codesfile

    def start_requests(self):
        url0 = 'http://qt.gtimg.cn/q=s_pk{}'
        url1 = 'http://qt.gtimg.cn/q=s_{}'
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
                time.sleep(5)
                if not is_stock_opening():
                    time.sleep(10)
                    continue
            for each in codes:
                yield scrapy.Request(url=url0.format(code_to_symbol(each)),
                        meta={'nexturl': url1.format(code_to_symbol(each))},
                        dont_filter=True, callback=self.parse_handicap)
            if self.debug: return

    def parse_handicap(self, response):
        # self.logger.info(response.url)
        result = response.body.decode('gbk')
        res = self.re_handicap.search(result)
        if res is None:
            return
        data = res.groupdict()['data']
        code = res.groupdict()['code']
        values = data.split('~')
        if len(values) < 4:
            return
        item = TapeReadingItem()
        item['code'] = code
        item['b_big_deal']   = float('%.2f' % (100 * float(values[0])))
        item['b_small_deal'] = float('%.2f' % (100 * float(values[1])))
        item['s_big_deal']   = float('%.2f' % (100 * float(values[2])))
        item['s_small_deal'] = float('%.2f' % (100 * float(values[3])))
        yield scrapy.Request(url=response.meta['nexturl'], meta={'item': item},
                dont_filter=True, callback=self.parse_brief, priority=100)
        if self.debug: return

    def parse_brief(self, response):
        # self.logger.info(response.url)
        result = response.body.decode('gbk')
        res = self.re_brief.search(result)
        if res is None:
            return
        data = res.groupdict()['data']
        code = res.groupdict()['code']
        values = data.split('~')
        if len(values) < 10:
            return
        item = response.meta['item']
        if code != item['code']:
            self.logger.warn('code is not same')
            return
        item['unkown1'] = values[0]
        item['name']    = values[1]
        item['code']    = values[2]
        item['price']   = float(values[3])
        item['chg']     = float(values[4])
        item['pchg']    = float(values[5])
        item['volume']  = int(int(values[6])/100)
        item['amount']  = float(values[6])
        item['unkown2'] = float(values[6])
        item['tcap']    = float(values[6])
        item['rec_datetime'] = datetime.datetime.now()
        yield item

    def closed(self, reason):
        self.logger.info(reason)
