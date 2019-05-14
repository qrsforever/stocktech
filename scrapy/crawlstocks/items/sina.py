#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-05 18:07:27

import scrapy

class LatestQuotaItem(scrapy.Item):
    _id        = scrapy.Field() # code_datetime
    code       = scrapy.Field() # code
    name       = scrapy.Field() # 0 : 名字
    open       = scrapy.Field() # 1 : 今日开盘价
    settlement = scrapy.Field() # 2 : 昨日收盘价
    price      = scrapy.Field() # 3 : 当前价格
    high       = scrapy.Field() # 4 : 今日最高价
    low        = scrapy.Field() # 5 : 今日最低价
    b_p        = scrapy.Field() # 6 : 竞买价,即"买一"出价
    a_p        = scrapy.Field() # 7 : 竞卖价,即"卖一"要价
    volume     = scrapy.Field() # 8 : 成交量(单位:100手)
    amount     = scrapy.Field() # 9 : 成交金额(万元)
    b1_v       = scrapy.Field() # 10: 委买一
    b1_p       = scrapy.Field() # 11: 委买一 出价
    b2_v       = scrapy.Field() # 12: 买二
    b2_p       = scrapy.Field() # 13: 买二
    b3_v       = scrapy.Field() # 14: 买三
    b3_p       = scrapy.Field() # 15: 买三
    b4_v       = scrapy.Field() # 16: 买四
    b4_p       = scrapy.Field() # 17: 买四
    b5_v       = scrapy.Field() # 18: 买五
    b5_p       = scrapy.Field() # 19: 买五
    a1_v       = scrapy.Field() # 20: 委卖一
    a1_p       = scrapy.Field() # 21: 委卖一 要价
    a2_v       = scrapy.Field() # 22: 卖二
    a2_p       = scrapy.Field() # 23: 卖二
    a3_v       = scrapy.Field() # 24: 卖三
    a3_p       = scrapy.Field() # 25: 卖三
    a4_v       = scrapy.Field() # 26: 卖四
    a4_p       = scrapy.Field() # 27: 卖四
    a5_v       = scrapy.Field() # 28: 卖五
    a5_p       = scrapy.Field() # 28: 卖五
    datetime   = scrapy.Field() # 30: 日期时间
