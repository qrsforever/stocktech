#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file xinhuanet.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-17 20:39:24

from crawlstocks.utils.send import send_mqtt

import json

class LeaderNewsPipeline(object):

    topic = '/stocktech/reminder/leadernews'

    def process_item(self, item, spider):
        send_mqtt(self.topic, json.dumps({
            'title': item['tag'],
            'brief': item['title'],
            'predict': 0,
            'body': item['url']
            }, ensure_ascii=False))
        return item
