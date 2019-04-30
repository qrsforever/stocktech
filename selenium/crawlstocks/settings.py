#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

# dir
TOP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..')
SELENIUM_DIR = os.path.join(TOP_PATH, 'selenium')
OUTPUT_DIR = os.path.join(TOP_PATH, 'output')
FILE_DIR = '/media/lidong/udisk/stocktech/files'

# logger
LOG_ENABLED = True
LOG_STDOUT = True
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s %(message)s'
LOG_FILE = os.path.join(OUTPUT_DIR, 'selenium.log')
BROWSER_LOG_FILE = os.path.join(OUTPUT_DIR, 'browser.log')

# browser
FIREFOX_BINARY_PATH = os.path.join('/usr/bin/', 'firefox')
FIREFOX_EXECUTABLE_PATH = os.path.join(SELENIUM_DIR, 'bin', 'geckodriver_linux64_v0.24.0')
FIREFOX_IMPLICITLY_WAIT = 3
FIREFOX_LOAD_TIMEOUT = 6000

# gu.qq.com: user password
GU_QQ_USERNAME = os.environ.get('U1', '985612771@qq.com')
GU_QQ_PASSWORD = os.environ.get('P1', '123456')

# mongodb
DB_URI = 'mongodb://localhost:27027/'
DB_NAME = 'stocktech'

# files
GU_QQ_COOKIES_FILE = os.path.join(FILE_DIR, 'gu_qq_cookies.txt')
OPTIONAL_CODES_FILE = os.path.join(FILE_DIR, 'optinal_codes.txt')
