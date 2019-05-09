#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:00:59

from crawlstocks.utils.send import send_mail

class RealtimeQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item


#####################################################################################

class CashFlowPipeline(object):

    def process_item(self, item, spider):
        return item

class TapeReadingPipeline(object):

    def process_item(self, item, spider):
        if item['b_big_deal'] > 30 or \
                item['b_big_deal'] + item['b_small_deal'] > 75:
            body = """<html><body>
            <h2>大单提醒</h2>
            <table align='center' cellpadding='10' cellspacing="4">
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
            </table></body></html>"""
            send_mail(body.format(
                '股票名', item['name'],
                '股票码', item['code'],
                '当前价', item['price'],
                '涨跌额', item['chg'],
                '涨跌率', item['pchg'],
                '成交量', item['volume'],
                '成交额', item['amount'],
                '买大单', item['b_big_deal'],
                '买小单', item['b_small_deal']), 'html')
        return item
