#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:00:59

from crawlstocks.utils.send import send_mail
from crawlstocks.utils.send import send_mqtt

import json, time

class RealtimeQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item


#####################################################################################

class CashFlowPipeline(object):

    def process_item(self, item, spider):
        return item

class TapeReadingPipeline(object):

    topic = '/stocktech/reminder/tapereading'
    rec_time = time.time()

    def process_item(self, item, spider):

        title = None
        predict = 0
        if item['b_big_deal'] > 45 or \
                (item['b_big_deal'] > 15 and \
                item['b_big_deal'] + item['b_small_deal'] > 70):
            title = "大买单提醒"
            predict = 1

        if item['s_big_deal'] > 45 or \
                (item['s_big_deal'] > 15 and \
                item['s_big_deal'] + item['s_small_deal'] > 70):
            title = "大卖单提醒"
            predict = -1

        if title is None:
            return item

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
            <tr><td>{}</td><td>{}</td></tr>
            <tr><td>{}</td><td>{}</td></tr>
            <tr><td>{}</td><td>{}</td></tr>
        </table></body></html>"""
        payload = body.format(
            '股票名', item['name'],
            '股票码', item['code'],
            '当前价', item['price'],
            '涨跌额', item['chg'],
            '涨跌率', item['pchg'],
            '成交量', item['volume'],
            '成交额', item['amount'],
            '大买单', item['b_big_deal'],
            '小买单', item['b_small_deal'],
            '大卖单', item['s_big_deal'],
            '小卖单', item['s_small_deal'],
            '时间', item['rec_datetime'].strftime('%Y%m%d-%H:%M:%S'))
        send_mail(payload, 'html')
        send_mqtt(self.topic, json.dumps({
            'title': title,
            'brief': '%s %8s %8s %8s %10s' % (
                item['name'], item['code'],
                item['price'], item['pchg'],
                item['rec_datetime'].strftime('%H:%M:%S')),
            'predict': predict,
            'body': payload
            }, ensure_ascii=False))
        self.rec_time = time.time()
        return item
