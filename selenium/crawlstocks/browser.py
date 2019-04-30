#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from crawlstocks.utils.common import Singleton
from crawlstocks.utils.logger import Logger

import crawlstocks.settings as settings

@Singleton
class Browser(object):
    logger = Logger(__name__)
    driver = None
    def __init__(self, brw_name):
        print(brw_name)
        if brw_name == 'firefox':
            profile = FirefoxProfile()
            # Disable CSS
            # profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            # profile.set_preference('permissions.default.image', 2)
            # Disable flash
            # profile.set_preference('plugin.state.flash', '2')
            # Disable histroy
            profile.set_preference( "places.history.enabled", False)
            self.driver = webdriver.Firefox(
                    firefox_profile = profile,
                    firefox_binary = settings.FIREFOX_BINARY_PATH,
                    executable_path = settings.FIREFOX_EXECUTABLE_PATH,
                    log_path = settings.BROWSER_LOG_FILE)
            self.driver.implicitly_wait(settings. FIREFOX_IMPLICITLY_WAIT)
            self.driver.maximize_window()
        elif brw_name == 'chrome':
            self.logger.warn('not impl')
        else:
            self.logger.warn('not impl')
