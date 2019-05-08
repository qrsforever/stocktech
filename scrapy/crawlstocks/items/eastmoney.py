#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

class StockUrlItem(scrapy.Item):
    stock_url = scrapy.Field()

class StockCwzbItem(scrapy.Item):
    name                  = scrapy.Field() # 股票名称
    code                  = scrapy.Field() # 股票代码
    report_date           = scrapy.Field() # 截止日期
    eps                   = scrapy.Field() # 每股收益(元)
    deducted_eps          = scrapy.Field() # 扣非每股收益(元)
    diluted_eps           = scrapy.Field() # 稀释每股收益(元)
    net_profit            = scrapy.Field() # 净利润(亿元）
    net_profit_yony       = scrapy.Field() # 净利润同比增长(%)
    net_profit_monm       = scrapy.Field() # 净利润滚动环比增长(%)
    ROE_WA                = scrapy.Field() # 加权净资产收益率(%）
    ROE_ED                = scrapy.Field() # 摊薄净资产收益率(%)
    gross_profit          = scrapy.Field() # 毛利率(%）
    eff_tax_rate          = scrapy.Field() # 实际税率(%)
    deposit_gross_rate    = scrapy.Field() # 预收款/营业收入
    cashflow_gross_rate   = scrapy.Field() # 销售现金流/营业收入
    total_assets_turnover = scrapy.Field() # 总资产周转率(次)
    liability_assets_rate = scrapy.Field() # 资产负债率(%)
    debt_flow_total_rate  = scrapy.Field() # 流动负债/总负债(%)
