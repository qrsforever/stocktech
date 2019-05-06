#!/usr/bin/python3
# -*- coding: utf-8 -*-

class RealtimeQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
