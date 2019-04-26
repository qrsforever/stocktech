#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

class CHDDataItem(scrapy.Item):
    _id = scrapy.Field()         # 股票代码_日期
    name = scrapy.Field()        # 股票名称
    code = scrapy.Field()        # 股票代码
    date = scrapy.Field()        # 日期
    tclose = scrapy.Field()      # 收盘价
    high = scrapy.Field()        # 最高价
    low = scrapy.Field()         # 最低价
    topen = scrapy.Field()       # 开盘价
    lclose = scrapy.Field()      # 前收盘
    chg = scrapy.Field()         # 涨跌额
    pchg = scrapy.Field()        # 涨跌幅
    turnover = scrapy.Field()    # 换手率
    voturnover = scrapy.Field()  # 成交量
    vaturnover = scrapy.Field()  # 成交金额
    tcap = scrapy.Field()        # 总市值
    mcap = scrapy.Field()        # 流通市值
