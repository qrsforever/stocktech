#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file eastmoney.py
# @brief 
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 23:46:58

class StockUrlPipeline(object):
    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('STOCK_URLS_FILE'))

    def process_item(self, item, spider):
        try:
            self.file.write(item['stock_url'])
            self.file.write('\n')
        except Exception as e:
             spider.logger.info("write error:", e)
        return item

    def open_spider(self, spider):
        try:
            self.file = open(self.filepath, "w+", encoding='utf-8')
        except Exception as e:
            spider.logger.info("open error:", e)

    def close_spider(self, spider):
        try:
            self.file.close()
        except:
            spider.logger.info("close error")


#####################################################################################


class StockCwzbPipeline(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.fmt = ""
        for i in range(13):
            self.fmt = self.fmt + '{%d:^10}\t' % i
        self.fmt = self.fmt + '\n'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('STOCK_CWZB_FILE'))

    def process_item(self, item, spider):
        try:
            self.file.write(self.fmt.format(
                item['name'],
                item['code'],
                item['report_date'],
                item['eps'],
                item['deducted_eps'],
                item['diluted_eps'],
                item['net_profit'],
                item['net_profit_yony'],
                item['net_profit_monm'],
                item['ROE_WA'],
                item['ROE_ED'],
                item['gross_profit'],
                item['eff_tax_rate'],
                item['deposit_gross_rate'],
                item['cashflow_gross_rate'],
                item['total_assets_turnover'],
                item['liability_assets_rate'],
                item['debt_flow_total_rate'],
                chr(12288)))
        except Exception as e:
             spider.logger.info("write error:", e)
        return item

    def open_spider(self, spider):
        titles = (
                '股票名称',
                '股票代码',
                '截止日期',
                '每股收益(元)',
                '扣非每股收益(元)',
                '稀释每股收益(元)',
                '净利润(亿元)',
                '净利润同比增长(%)',
                '净利润滚动环比增长(%)',
                '加权净资产收益率(%)',
                '摊薄净资产收益率(%)',
                '毛利率(%)',
                '实际税率(%)',
                '预收款/营业收入',
                '销售现金流/营业收入',
                '总资产周转率(次)',
                '资产负债率(%)',
                '流动负债/总负债(%)',
                )
        try:
            self.file = open(self.filepath, "w+", encoding='utf-8')
            for each in titles:
                self.file.write('{0} '.format(each, chr(12288)))
            self.file.write('\n')
        except Exception as e:
            spider.logger.info("open error:", e)

    def close_spider(self, spider):
        try:
            self.file.close()
        except:
            spider.logger.info("close error")

