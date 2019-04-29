#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class TickDetailPipeline(object):
    def __init__(self, uri, db, col):
        self.mongo_uri = uri
        self.mongo_db = db
        self.mongo_collection = col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DB_URI', 'mongodb://localhost:27027/'),
                crawler.settings.get('DB_NAME', 'stocktech'),
                crawler.settings.get('DB_TICKDETAIL_COLLECTION_NAME', 'tickdetail'))

    def process_item(self, item, spider):
        try:
            # item is subclass of dict
            if self.col:
                self.col.update_one({'_id': item['_id']},
                        {'$set': dict(item)}, upsert = True)
        except Exception as e:
             spider.logger.info("write error: ", repr(e))
        return item

    def open_spider(self, spider):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            found = False
            for name in self.db.list_collection_names():
                if name == self.mongo_collection:
                    found = True
                    break
            if found:
                self.col = self.db[self.mongo_collection]
            else:
                # 固定大小DB, 最大200MB, 最大条目200万条, 满足一条即可
                self.col = self.db.create_collection(self.mongo_collection,
                        capped=True, size=200000000, max=200000000)
        except Exception as e:
            spider.logger.info("open error:", repr(e))

    def close_spider(self, spider):
        try:
            self.client.close()
        except:
            spider.logger.info("close error")
