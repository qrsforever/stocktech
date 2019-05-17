#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:01:12

import os
import datetime

class LatestQuotaPipeline(object):
    def __init__(self, tmpdir):
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.filepath = os.path.join(tmpdir, ts + '.' + 'latestquota.txt')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('TMP_DIR'))

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
        buy_avg = (buy1 + buy2 + buy3 + buy4 + buy5) / total_buy_vol
        sell_avg = (sell1 + sell2 + sell3 + sell4 + sell5) / total_sell_vol
        buy_v_rate = 100 * total_buy_vol/total
        sell_v_rate = 100 * total_sell_vol/total
        buy_p_rate = (item['price'] - buy_avg) * 100 / (sell_avg - buy_avg)
        sell_p_rate = (sell_avg-item['price']) * 100 / (sell_avg - buy_avg)

        spider.logger.info('%s %s %.2f%% vs %.2f%% | %.2f%% vs %.2f%% | '\
                ' %.2f vs %.2f | %.2f %.2f | %.2f %.2f ' % \
                (item['code'], item['name'], buy_v_rate, sell_v_rate, buy_p_rate,
                    sell_p_rate, buy_avg, sell_avg, item['price'], item['settlement'],
                    buy_vol2_rate, sell_vol2_rate))
        try:
            self.file.write('%s %s %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %s\n' % \
                (item['code'], item['name'], buy_v_rate, sell_v_rate, buy_p_rate,
                    sell_p_rate, buy_avg, sell_avg, item['price'], item['settlement'],
                    buy_vol2_rate, sell_vol2_rate, item['datetime'].strftime('%Y%m%d %H:%M:%S')))
        except Exception as e:
             spider.logger.info("write error:", e)
        return item

    def open_spider(self, spider):
        try:
            self.file = open(self.filepath, "w", encoding='utf-8')
            self.file.write('{} {} {} {} {} {} {} {} {} {} {} {} {}\n'
                    .format('股票码', '股票名', '买量率', '卖量率', '买距比', '卖距比', \
                            '买均价', '卖均价', '当前价', '昨收',
                            '前二买', '前二卖', '日期', chr(12288)))
        except Exception as e:
            spider.logger.info("open error:", e)

    def close_spider(self, spider):
        try:
            self.file.close()
        except:
            spider.logger.info("close error")

