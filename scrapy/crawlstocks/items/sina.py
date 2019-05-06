#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

class LatestQuotaItem(scrapy.Item):
    _id = scrapy.Field()        # code
    code = scrapy.Field()       # code
    name = scrapy.Field()       # 0 : 名字
    curr_open = scrapy.Field()  # 1 : open,今日开盘价
    pre_close = scrapy.Field()  # 2 : pre_close,昨日收盘价
    price = scrapy.Field()      # 3 : price,当前价格
    high = scrapy.Field()       # 4 : high,今日最高价
    low = scrapy.Field()        # 5 : low,今日最低价
    bid = scrapy.Field()        # 6 : bid,竞买价,即"买一"报价
    ask = scrapy.Field()        # 7 : ask,竞卖价,即"卖一"报价
    volumn = scrapy.Field()     # 8 : volumn,成交量(单位:1手, 使用要除以100)
    amount = scrapy.Field()     # 9 : amount,成交金额(元 CNY)
    b1_v = scrapy.Field()       # 10: 委买一(笔数 bid volume) 出价
    b1_p = scrapy.Field()       # 11: 委买一(价格 bid price)
    b2_v = scrapy.Field()       # 12: 买二
    b2_p = scrapy.Field()       # 13: 买二
    b3_v = scrapy.Field()       # 14: 买三
    b3_p = scrapy.Field()       # 15: 买三
    b4_v = scrapy.Field()       # 16: 买四
    b4_p = scrapy.Field()       # 17: 买四
    b5_v = scrapy.Field()       # 18: 买五
    b5_p = scrapy.Field()       # 19: 买五
    a1_v = scrapy.Field()       # 20: 委卖一(笔数 ask volume) 要价
    a1_p = scrapy.Field()       # 21: 委卖一(价格 ask price)
    a2_v = scrapy.Field()       # 22: 卖二
    a2_p = scrapy.Field()       # 23: 卖二
    a3_v = scrapy.Field()       # 24: 卖三
    a3_p = scrapy.Field()       # 25: 卖三
    a4_v = scrapy.Field()       # 26: 卖四
    a4_p = scrapy.Field()       # 27: 卖四
    a5_v = scrapy.Field()       # 28: 卖五
    a5_p = scrapy.Field()       # 28: 卖五
    datetime = scrapy.Field()   # 30: 日期时间
