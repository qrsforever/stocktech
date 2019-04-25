# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlstocksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GuchengStockCodeItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()

class GuchengStockInfoItem(scrapy.Item):
    name = scrapy.Field()            # 股票名称
    code = scrapy.Field()            # 股票代码
    report_date = scrapy.Field()     # 截止日期
    earning_ps = scrapy.Field()      # 每股收益（元）
    net_assets_ps = scrapy.Field()   # 每股净资产（元）
    net_profit = scrapy.Field()      # 净利润（亿元）
    net_asset = scrapy.Field()       # 净资产（亿元）
    gross_sales = scrapy.Field()     # 营业收入（亿元）
    ROE = scrapy.Field()             # 净资产收益率（%）
    PER = scrapy.Field()             # 市盈率
    PBR = scrapy.Field()             # 市净率
    cash_flow_ps = scrapy.Field()    # 每股现金流净额（元）
    gross_profit = scrapy.Field()    # 销售毛利率（%）

class EastmoneyStockUrlItem(scrapy.Item):
    stock_url = scrapy.Field()

class EastmoneyStockCwzbItem(scrapy.Item):
    name = scrapy.Field()                  # 股票名称
    code = scrapy.Field()                  # 股票代码
    report_date = scrapy.Field()           # 截止日期
    eps = scrapy.Field()                   # 每股收益(元)
    deducted_eps = scrapy.Field()          # 扣非每股收益(元)
    diluted_eps = scrapy.Field()           # 稀释每股收益(元)
    net_profit = scrapy.Field()            # 净利润(亿元）
    net_profit_yony = scrapy.Field()       # 净利润同比增长(%)
    net_profit_monm = scrapy.Field()       # 净利润滚动环比增长(%)
    ROE_WA = scrapy.Field()                # 加权净资产收益率(%）
    ROE_ED = scrapy.Field()                # 摊薄净资产收益率(%)
    gross_profit = scrapy.Field()          # 毛利率(%）
    eff_tax_rate = scrapy.Field()          # 实际税率(%)
    deposit_gross_rate = scrapy.Field()    # 预收款/营业收入
    cashflow_gross_rate = scrapy.Field()   # 销售现金流/营业收入
    total_assets_turnover = scrapy.Field() # 总资产周转率(次)
    liability_assets_rate = scrapy.Field() # 资产负债率(%)
    debt_flow_total_rate = scrapy.Field()  # 流动负债/总负债(%)

class QuotesCHDDataItem(scrapy.Item):
    _id = scrapy.Field()            # 股票代码_日期
    name = scrapy.Field()           # 股票名称
    code = scrapy.Field()           # 股票代码
    date = scrapy.Field()           # 日期
    tclose = scrapy.Field()         # 收盘价
    high = scrapy.Field()           # 最高价
    low = scrapy.Field()            # 最低价
    topen = scrapy.Field()          # 开盘价
    lclose = scrapy.Field()         # 前收盘
    chg = scrapy.Field()            # 涨跌额
    pchg = scrapy.Field()           # 涨跌幅
    turnover = scrapy.Field()       # 换手率
    voturnover = scrapy.Field()     # 成交量
    vaturnover = scrapy.Field()     # 成交金额
    tcap = scrapy.Field()           # 总市值
    mcap = scrapy.Field()           # 流通市值
