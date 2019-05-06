#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

# 实时成交量明细
class TickDetailItem(scrapy.Item):
    _id = scrapy.Field()        # 主键 = code_datetime
    code = scrapy.Field()       # 股票代码
    datetime = scrapy.Field()   # 交易时间
    price = scrapy.Field()      # 成交价格
    change = scrapy.Field()     # 涨跌额
    volume = scrapy.Field()     # 成交量(手)
    amount = scrapy.Field()     # 成交额(元)
    bstype = scrapy.Field()     # B 买入, S 卖出, M 中性盘

#####################################################################################

class RealtimeQuotaItem(scrapy.Item):
    _id = scrapy.Field()                  #
    name = scrapy.Field()                 # 1 : 名字
    code = scrapy.Field()                 # 2 : 代码
    price = scrapy.Field()                # 3 : 当前价格
    settlement = scrapy.Field()           # 4 : 昨收
    open = scrapy.Field()                 # 5 : 今开
    volume = scrapy.Field()               # 6 : 成交量 (100手)
    bid = scrapy.Field()                  # 7 : 外盘
    ask = scrapy.Field()                  # 8 : 内盘
    b1_p = scrapy.Field()                 # 9 : 买1
    b1_v = scrapy.Field()                 # 10: 买1量 (100手)
    b2_p = scrapy.Field()                 # 11:
    b2_v = scrapy.Field()                 # 12:
    b3_p = scrapy.Field()                 # 13:
    b3_v = scrapy.Field()                 # 14:
    b4_p = scrapy.Field()                 # 15:
    b4_v = scrapy.Field()                 # 16:
    b5_p = scrapy.Field()                 # 17:
    b5_v = scrapy.Field()                 # 18:
    a1_p = scrapy.Field()                 # 19: 卖1
    a1_v = scrapy.Field()                 # 20: 卖1量
    a2_p = scrapy.Field()                 # 21:
    a2_v = scrapy.Field()                 # 22:
    a3_p = scrapy.Field()                 # 23:
    a3_v = scrapy.Field()                 # 24:
    a4_p = scrapy.Field()                 # 25:
    a4_v = scrapy.Field()                 # 26:
    a5_p = scrapy.Field()                 # 27:
    a5_v = scrapy.Field()                 # 28:
    recent_trades = scrapy.Field()        # 29: 最近6笔成交
    datetime = scrapy.Field()             # 30: 时间
    chg = scrapy.Field()                  # 31: 涨跌
    pchg = scrapy.Field()                 # 32: 涨跌%
    high = scrapy.Field()                 # 33: 最高
    low = scrapy.Field()                  # 34: 最低
    price_volume_amount = scrapy.Field()  # 35: 价格/成交量(手)/成交额
    volume = scrapy.Field()               # 36: 成交量(100手)
    amount = scrapy.Field()               # 37: 成交额(万)
    turnover = scrapy.Field()             # 38: 换手率
    PE = scrapy.Field()                   # 39: 市盈率
    unknown = scrapy.Field()              # 40:
    high2 = scrapy.Field()                # 41: 最高2
    low2 = scrapy.Field()                 # 42: 最低2
    amplitude = scrapy.Field()            # 43: 振幅
    mcap = scrapy.Field()                 # 44: 流通市值
    tcap = scrapy.Field()                 # 45: 总市值
    PB = scrapy.Field()                   # 46: 市净率
    topest = scrapy.Field()               # 47: 涨停价
    lowest = scrapy.Field()               # 48: 跌停价
