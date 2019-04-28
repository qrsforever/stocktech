#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class CHDDataPipeline(object):
    def __init__(self, uri, db, col):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_collection = col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DB_HOST', 'mongodb://localhost:27017/'),
                crawler.settings.get('DB_NAME', 'stocktech'),
                crawler.settings.get('DB_CHDDATA_COLLECTION_NAME', 'chddata'))

    def process_item(self, item, spider):
        try:
            # item is subclass of dict
            self.col.update_one({'_id': item['_id']},
                    {'$set': dict(item)}, upsert = True)
        except Exception as e:
             spider.logger.info("write error: ", repr(e))
        return item

    def open_spider(self, spider):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.col = self.db[self.mongo_collection]
        except Exception as e:
            spider.logger.info("open error:", repr(e))

    def close_spider(self, spider):
        try:
            self.client.close()
        except:
            spider.logger.info("close error")