#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:01:12

from crawlstocks.utils.send import send_mail

class LatestQuotaPipeline(object):

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

        total = total_buy_vol + total_sell_vol
        buy = (buy1 + buy2 + buy3 + buy4 + buy5) / total_buy_vol
        sell = (sell1 + sell2 + sell3 + sell4 + sell5) / total_sell_vol
        buy_v_rate = round(100 * total_buy_vol/total, 2)
        sell_v_rate = round(100 * total_sell_vol/total, 2)
        buy_p_rate = round((item['price'] - buy) * 100 / (sell - buy), 2)
        sell_p_rate = round((sell-item['price']) * 100 / (sell - buy), 2)

        if sell_p_rate >= 73 or sell_p_rate <= 27:
            title="买强看涨提醒"
            if sell_p_rate > buy_p_rate:
                title="卖强看跌提醒"
            body = """<html><body>
            <h2>{}</h2>
            <table align='center' cellpadding='10' cellspacing="4">
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
                <tr><td>{}</td><td>{</td></tr>
            </table></body></html>"""
            send_mail(body.format(title,
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
                '时间', item['datetime'].strftime('%Y%m%d-%H:%M:%S')
                ), 'html')
        return item
