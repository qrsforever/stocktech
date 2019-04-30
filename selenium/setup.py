#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '',
    'author': '',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['crawlstocks'],
    'scripts': [],
    'name': 'crawlstocks'
}

setup(**config)
