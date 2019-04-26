#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class CHDDataPipeline(object):
    def __init__(self, host, name, table):
        self.mongo = MongoClient(host)
        self.db = self.mongo[name]
        self.table = self.db[table]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DB_HOST'),
                crawler.settings.get('DB_NAME'),
                crawler.settings.get('DB_CHDDATA_TABLE_NAME'))

    def process_item(self, item, spider):
        try:
            # item is subclass of dict
            self.table.update_one({'_id': item['_id']},
                    {'$set': item}, upsert = True)
        except Exception as e:
             spider.logger.info("write error: ", e)
        return item

    def open_spider(self, spider):
        try:
            pass
        except Exception as e:
            spider.logger.info("open error:", e)

    def close_spider(self, spider):
        try:
            self.mongo.close()
        except:
            spider.logger.info("close error")
