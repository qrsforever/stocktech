#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy

class CrawlErrorItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    tag = scrapy.Field()
    message = scrapy.Field()
    errtime = scrapy.Field()
