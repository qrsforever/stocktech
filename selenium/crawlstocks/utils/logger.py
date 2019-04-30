#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import crawlstocks.settings as settings

class Logger(object):
    logger = None
    enable = settings.LOG_ENABLED
    def __init__(self, name):
        if not self.enable:
            return

        # levels = {
                # 'DEBUG': logging.DEBUG,
                # 'INFO': logging.INFO,
                # 'WARNING': logging.WARNING,
                # 'ERROR': logging.ERROR,
                # 'CRITICAL': logging.CRITICAL
                # }
        logger = logging.getLogger(name)
        logger.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter(settings.LOG_FORMAT)

        try:
            # file handler
            if settings.LOG_FILE:
                fh = logging.FileHandler(settings.LOG_FILE)
                fh.setFormatter(formatter)
                logger.addHandler(fh)
        except:
            pass

        try:
            # console
            if settings.LOG_STDOUT:
                ch = logging.StreamHandler()
                ch.setFormatter(formatter)
                logger.addHandler(ch)
        except:
            pass
        self.logger = logger

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
