#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file sina.py
# @brief 
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-08 00:01:12


import os

class StockCodePipeline(object):
    def __init__(self, dir):
        self.filepath = os.path.join(dir, 'tencent.stockcode.txt')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('FILE_DIR'))

    def process_item(self, item, spider):
        try:
            self.file.write('{}\n'.format(item['code']))
        except Exception as e:
             spider.logger.info("write error:", e)
        return item

    def open_spider(self, spider):
        try:
            self.file = open(self.filepath, "w", encoding='utf-8')
        except Exception as e:
            spider.logger.info("open error:", e)

    def close_spider(self, spider):
        try:
            self.file.close()
        except:
            spider.logger.info("close error")


#####################################################################################
