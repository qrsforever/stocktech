# -*- coding: utf-8 -*-

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, type):
        #  self.user_agent_list = agents
        self.ua = UserAgent(use_cache_server=True)
        self.ua_type = type

    @classmethod
    def from_crawler(cls, crawler):
        #  return cls(crawler.settings.get('USER_AGENT_LIST'))
        return cls(crawler.settings.get('RANDOM_UA_TYPE', 'random'))

    def process_request(self, request, spider):
        #  request.headers['User-Agent'] = random.choice(self.user_agent_list)
        # 通过配置文件的随机类型进行调用
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers['User-Agent'] = get_ua()

class RandomProxyMiddleware(object):
    def __init__(self, proxes):
        self.user_proxy_list = proxes

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_PROXY_LIST'))

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://%s' % random.choice(self.user_proxy_list)
