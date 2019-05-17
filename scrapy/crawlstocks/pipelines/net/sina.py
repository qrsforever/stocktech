#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:01:12

from crawlstocks.utils.send import send_mail
from crawlstocks.utils.send import send_mqtt

import json, time

class LatestQuotaPipeline(object):

    topic = '/stocktech/reminder/latestquota'
    rec_time = time.time()

    def process_item(self, item, spider):
        buy1 = item['b1_v'] * item['b1_p']  # buy
        buy2 = item['b2_v'] * item['b2_p']
        buy3 = item['b3_v'] * item['b3_p']
        buy4 = item['b4_v'] * item['b4_p']
        buy5 = item['b5_v'] * item['b5_p']

        sell1 = item['a1_v'] * item['a1_p'] # sell
        sell2 = item['a2_v'] * item['a2_p']
        sell3 = item['a3_v'] * item['a3_p']
        sell4 = item['a4_v'] * item['a4_p']
        sell5 = item['a5_v'] * item['a5_p']

        total_buy_vol = item['b1_v'] + item['b2_v'] + item['b3_v'] + item['b4_v'] + item['b5_v']
        total_sell_vol = item['a1_v'] + item['a2_v'] + item['a3_v'] + item['a4_v'] + item['a5_v']

        if total_buy_vol == 0:
            spider.logger.warn('buy volum is 0')
            return item
        if total_sell_vol == 0:
            spider.logger.warn('sell volum is 0')
            return item

        buy_vol2_rate = round(100 * (item['b1_v'] + item['b2_v']) / total_buy_vol, 2)
        sell_vol2_rate = round(100 * (item['a1_v'] + item['a2_v']) / total_sell_vol, 2)

        total = total_buy_vol + total_sell_vol
        buy = (buy1 + buy2 + buy3 + buy4 + buy5) / total_buy_vol
        sell = (sell1 + sell2 + sell3 + sell4 + sell5) / total_sell_vol
        buy_v_rate = round(100 * total_buy_vol/total, 2)
        sell_v_rate = round(100 * total_sell_vol/total, 2)
        buy_p_rate = round((item['price'] - buy) * 100 / (sell - buy), 2)
        sell_p_rate = round((sell-item['price']) * 100 / (sell - buy), 2)

        if sell_p_rate >= 73 or sell_p_rate <= 27:
            if time.time() - self.rec_time < 20: return item
            if item['b_p'] == item['price']:
                title="看涨提醒"
                up = 1
            elif item['a_p'] == item['price']:
                title="看跌提醒"
                up = -1
            else:
                title="未知提醒"
                up = 0
            body = """<html><body>
            <h2>{}</h2>
            <table align='center' cellpadding='10' cellspacing="6">
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}%</td></tr>
                <tr><td>{}</td><td>{}</td></tr>
            </table></body></html>"""
            payload = body.format(title,
                '股票名', item['name'],
                '股票码', item['code'],
                '当前价', item['price'],
                '昨收价', item['settlement'],
                '竞买价', item['b_p'],
                '竟卖价', item['a_p'],
                '买量比', buy_v_rate,
                '卖量比', sell_v_rate,
                '买价比', buy_p_rate,
                '卖价比', sell_p_rate,
                '前二买', buy_vol2_rate,
                '前二卖', sell_vol2_rate,
                '时间', item['datetime'].strftime('%Y%m%d-%H:%M:%S'))
            send_mail(payload, 'html')

            send_mqtt(self.topic, json.dumps({
                'title': title,
                'brief': '%s %8s %8s %8s %10s' % (
                    item['name'], item['code'],
                    item['price'], item['settlement'],
                    item['datetime'].strftime('%H:%M:%S')),
                'predict': up,
                'body': payload
                }, ensure_ascii=False))
            self.rec_time = time.time()
        return item
