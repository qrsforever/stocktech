#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-07 15:32:26

import scrapy

class StockCodeItem(scrapy.Item):
    code = scrapy.Field()

# 实时成交量明细
class TickDetailItem(scrapy.Item):
    _id      = scrapy.Field() # 主键 = code_datetime
    code     = scrapy.Field() # 股票代码
    datetime = scrapy.Field() # 交易时间
    price    = scrapy.Field() # 成交价格
    change   = scrapy.Field() # 涨跌额
    volume   = scrapy.Field() # 成交量(手)
    amount   = scrapy.Field() # 成交额(元)
    bstype   = scrapy.Field() # B买入, S卖出, M中性盘

#####################################################################################

class RealtimeQuotaItem(scrapy.Item):
    _id                 = scrapy.Field() #
    name                = scrapy.Field() #  1: 名字
    code                = scrapy.Field() #  2: 代码
    price               = scrapy.Field() #  3: 当前价格
    settlement          = scrapy.Field() #  4: 昨收
    open                = scrapy.Field() #  5: 今开
    volume              = scrapy.Field() #  6: 成交量 (100手)
    b_v                 = scrapy.Field() #  7: 外盘B(uy) 主动性买盘
    a_v                 = scrapy.Field() #  8: 内盘S(ell) 主动性抛盘
    b1_p                = scrapy.Field() #  9: 买1
    b1_v                = scrapy.Field() # 10: 买1量 (100手)
    b2_p                = scrapy.Field() # 11:
    b2_v                = scrapy.Field() # 12:
    b3_p                = scrapy.Field() # 13:
    b3_v                = scrapy.Field() # 14:
    b4_p                = scrapy.Field() # 15:
    b4_v                = scrapy.Field() # 16:
    b5_p                = scrapy.Field() # 17:
    b5_v                = scrapy.Field() # 18:
    a1_p                = scrapy.Field() # 19: 卖1
    a1_v                = scrapy.Field() # 20: 卖1量
    a2_p                = scrapy.Field() # 21:
    a2_v                = scrapy.Field() # 22:
    a3_p                = scrapy.Field() # 23:
    a3_v                = scrapy.Field() # 24:
    a4_p                = scrapy.Field() # 25:
    a4_v                = scrapy.Field() # 26:
    a5_p                = scrapy.Field() # 27:
    a5_v                = scrapy.Field() # 28:
    recent_trades       = scrapy.Field() # 29: 最近6笔成交
    datetime            = scrapy.Field() # 30: 时间
    chg                 = scrapy.Field() # 31: 涨跌
    pchg                = scrapy.Field() # 32: 涨跌%
    high                = scrapy.Field() # 33: 最高
    low                 = scrapy.Field() # 34: 最低
    price_volume_amount = scrapy.Field() # 35: 价格/成交量(手)/成交额
    volume              = scrapy.Field() # 36: 成交量(100手)
    amount              = scrapy.Field() # 37: 成交额(万)
    turnover            = scrapy.Field() # 38: 换手率
    PE                  = scrapy.Field() # 39: 市盈率
    unknown             = scrapy.Field() # 40:
    high2               = scrapy.Field() # 41: 最高2
    low2                = scrapy.Field() # 42: 最低2
    amplitude           = scrapy.Field() # 43: 振幅
    mcap                = scrapy.Field() # 44: 流通市值
    tcap                = scrapy.Field() # 45: 总市值
    PB                  = scrapy.Field() # 46: 市净率
    topest              = scrapy.Field() # 47: 涨停价
    lowest              = scrapy.Field() # 48: 跌停价

#####################################################################################

class CashFlowItem(scrapy.Item):
    _id           = scrapy.Field()
    code          = scrapy.Field() # 0: 股票代码
    main_in       = scrapy.Field() # 1: 主力流入(万)
    main_out      = scrapy.Field() # 2: 主力流出(万)
    main_net      = scrapy.Field() # 3: 主力净流入
    main_net_rate = scrapy.Field() # 4: 主力净流入百分比: 主力净流入/主力总资金 ?
    priv_in       = scrapy.Field() # 5: 散户流入
    priv_out      = scrapy.Field() # 6: 散户流出
    priv_net      = scrapy.Field() # 7: 散户净流入
    priv_net_rate = scrapy.Field() # 8: 散户净流入百分比: 散户净流入/散户总资金 ?
    total_cash    = scrapy.Field() # 9: 资金流入流出总和1+2+5+6 (?)
    unkown1       = scrapy.Field() # 10: 未知
    unkown2       = scrapy.Field() # 11: 未知
    name          = scrapy.Field() # 12: 名字
    date          = scrapy.Field() # 13: 日期
    before_day1   = scrapy.Field() # 14: 前1日的(日期^净流入^净流出)
    before_day2   = scrapy.Field() # 15: 前2日的(日期^净流入^净流出)
    before_day3   = scrapy.Field() # 16: 前3日的(日期^净流入^净流出)
    before_day4   = scrapy.Field() # 17: 前4日的(日期^净流入^净流出)
    unkown3       = scrapy.Field() # 18:
    unkown4       = scrapy.Field() # 19:
    datetime      = scrapy.Field() # 20: 日期时间戳
    

#####################################################################################


class TapeReadingItem(scrapy.Item):
    _id          = scrapy.Field()
    rec_datetime = scrapy.Field() # 爬取的时间

    unkown1      = scrapy.Field() # 0: 未知
    name         = scrapy.Field() # 1: 股票名称
    code         = scrapy.Field() # 2: 股票代码
    price        = scrapy.Field() # 3: 当前价格
    chg          = scrapy.Field() # 4: 涨跌
    pchg         = scrapy.Field() # 5: 涨跌%
    volume       = scrapy.Field() # 6: 成交量(100手)
    amount       = scrapy.Field() # 7: 成交额(万)
    unkown2      = scrapy.Field() # 8:
    tcap         = scrapy.Field() # 9: 总市值

    b_big_deal   = scrapy.Field() # 0: 买盘大单 (100%)
    b_small_deal = scrapy.Field() # 1: 买盘小单
    s_big_deal   = scrapy.Field() # 2: 卖盘大单
    s_small_deal = scrapy.Field() # 3: 卖盘小单

