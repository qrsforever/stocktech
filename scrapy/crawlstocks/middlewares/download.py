#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scrapy import signals

from twisted.internet.error import ConnectionRefusedError
from twisted.internet.error import TimeoutError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from crawlstocks.exceptions import DownloadException

# from scrapy.http import Response, Request

class DebugMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        spider.logger.info('requst head: %s' % request.headers)
        # spider.logger.info("request cookie: %s" % request.headers.getlist('Cookie'))
        return None

    def process_response(self, request, response, spider):
        spider.logger.info('response head: %s' % response.headers)
        # spider.logger.info("response cookie: %s" % response.headers.getlist('Set-Cookie'))
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#####################################################################################

class CatchExceptionMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, ConnectionRefusedError):
            raise DownloadException("ConnectionRefusedError")
        elif isinstance(exception, TCPTimedOutError):
            raise DownloadException("TCPTimedOutError")
        elif isinstance(exception, DNSLookupError):
            raise DownloadException("DNSLookupError")
        elif isinstance(exception, TimeoutError):
            raise DownloadException("TimeoutError")
        elif isinstance(exception, DNSLookupError):
            raise DownloadException("DNSLookupError")
        elif isinstance(exception, HttpError):
            raise DownloadException("HttpError")
        else:
            spider.logger.warn('Middleware: %s exception caught',
                    exception.__class__.__name__)
