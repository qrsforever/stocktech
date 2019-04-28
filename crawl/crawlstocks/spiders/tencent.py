#!/usr/bin/python3
# -*- coding: utf-8 -*-

import scrapy
from io import StringIO
from datetime import datetime
from pymongo import MongoClient

from crawlstocks.items.netease163 import CHDDataItem
from crawlstocks.exceptions import DownloadException
from crawlstocks.items.items import CrawlErrorItem

class CrawlChdDataSpider(scrapy.Spider):
    pass


#####################################################################################
