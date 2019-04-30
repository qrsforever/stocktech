#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

# 实时成交量明细
class TickDetailItem(scrapy.Item):
    _id = scrapy.Field()    # 主键 = code_time
    code = scrapy.Field()   # 股票代码
    time = scrapy.Field()   # 交易时间
    price = scrapy.Field()  # 成交价格
    change = scrapy.Field() # 涨跌额
    volume = scrapy.Field() # 成交量(手)
    amount = scrapy.Field() # 成交额(元)
    bstype = scrapy.Field() # B 买入, S 卖出, M 中性盘
