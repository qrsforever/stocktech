#!/usr/bin/python3
# -*- coding: utf-8 -*-

class LatestQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        bid1 = item['b1_v'] * item['b1_p'] # sell
        bid2 = item['b2_v'] * item['b2_p']
        bid3 = item['b3_v'] * item['b3_p']
        bid4 = item['b4_v'] * item['b4_p']
        bid5 = item['b5_v'] * item['b5_p']

        ask1 = item['a1_v'] * item['a1_p'] # buy
        ask2 = item['a2_v'] * item['a2_p']
        ask3 = item['a3_v'] * item['a3_p']
        ask4 = item['a4_v'] * item['a4_p']
        ask5 = item['a5_v'] * item['a5_p']

        total_bid_vol = item['b1_v'] + item['b2_v'] + item['b3_v'] + item['b4_v'] + item['b5_v']
        total_ask_vol = item['a1_v'] + item['a2_v'] + item['a3_v'] + item['a4_v'] + item['a5_v']

        if total_bid_vol == 0:
            spider.logger.warn('bid volum is 0')
            return
        if total_ask_vol == 0:
            spider.logger.warn('ask volum is 0')
            return

        total = total_bid_vol + total_ask_vol
        bid = (bid1 + bid2 + bid3 + bid4 + bid5) / total_bid_vol
        ask = (ask1 + ask2 + ask3 + ask4 + ask5) / total_ask_vol
        bid_per = (item['price'] - bid) * 100 / (ask - bid)
        ask_per = (ask-item['price']) * 100 / (ask - bid)
        spider.logger.info('出价量比: %.2f vs 要价量比: %.2f total: %.2f' % (100 * total_bid_vol/total,
            100 * total_ask_vol/total, total))



        spider.logger.info('出价均值:%.2f vs 要价均值:%.2f [出价比:%.2f%% %.2f 要价比:%.2f%%]' %
                (bid, ask, bid_per, item['price'], ask_per))

