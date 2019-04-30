#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from crawlstocks.task import *

if __name__ == "__main__":
    sys.path.append('.')
    len = len(sys.argv)
    if len < 2:
        print("invalid input")
        exit()
    if sys.argv[1] == 'list':
        i = 1
        print("==================================\n")
        for each in os.listdir('crawlstocks/task'):
            if each[0] == '_':
                continue
            print('[%d] task: crawl %s' % (i, each.split('.')[0]))
            i += 1
        print("\n==================================")
    elif sys.argv[1]  == 'crawl':
        if len == 3:
            try:
                eval('crawl_' + sys.argv[2])()
            except NameError:
                print("not found task: %s" % sys.argv[2])
            except Exception as e:
                print(e)
    else:
        print('invalid input')
