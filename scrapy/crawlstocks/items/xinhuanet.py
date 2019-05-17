#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file xinhuanet.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-17 19:59:36

import scrapy

# 领导人新闻
class LeaderNewsItem(scrapy.Item):
    url      = scrapy.Field() # 新闻地址
    tag      = scrapy.Field() # 指示批示 致电致信 考察调研 会议活动
    title    = scrapy.Field() # 新闻标题
    html     = scrapy.Field() # 新闻内容
    datetime = scrapy.Field() # 新闻时间

