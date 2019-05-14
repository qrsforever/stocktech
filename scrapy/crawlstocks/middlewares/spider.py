#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file spider.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-14 10:03:02

class CatchExceptionMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        spider.logger.warn('Middleware: %s exception caught', exception.__class__.__name__)
        method = '{}.process_spider_exception'.format(self.__class__.__name__)
        yield {'processed': [method]}

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
