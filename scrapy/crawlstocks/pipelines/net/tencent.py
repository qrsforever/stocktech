#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:00:59

from crawlstocks.utils.send import send_mail
import time

class RealtimeQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item


#####################################################################################

class CashFlowPipeline(object):

    def process_item(self, item, spider):
        return item

class TapeReadingPipeline(object):

    rec_time = time.time()

    def process_item(self, item, spider):
        if item['b_big_deal'] > 45 or \
               (item['b_big_deal'] > 15 and \
                item['b_big_deal'] + item['b_small_deal'] > 70):
            if time.time() - self.rec_time < 20: return item

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
                '大买单', item['b_big_deal'],
                '小买单', item['b_small_deal']), 'html')
            self.rec_time = time.time()
        return item
