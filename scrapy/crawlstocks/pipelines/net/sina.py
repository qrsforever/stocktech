#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:01:12

class LatestQuotaPipeline(object):

    def process_item(self, item, spider):
        spider.logger.info(item)
        return item
