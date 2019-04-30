#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scrapy.exceptions import IgnoreRequest

class DownloadException(IgnoreRequest):
    def __init__(self, *args, **kwargs):
        super(DownloadException, self).__init__(*args, **kwargs)

class SpiderException(IgnoreRequest):
    def __init__(self, *args, **kwargs):
        super(SpiderException, self).__init__(*args, **kwargs)
