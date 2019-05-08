#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file tencent.py
# @brief 
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:00:59


class RealtimeQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item


#####################################################################################

class CashFlowPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item
