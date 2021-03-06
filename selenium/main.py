#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file main.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-11 09:47:08

import sys
import os

from xvfbwrapper import Xvfb
from crawlstocks.task import *

def help():
    print('./main.py list|task_name|task_number(is one of list output')

if __name__ == "__main__":
    sys.path.append('.')
    if len(sys.argv) < 2:
        help()
        exit()

    task = []
    for each in os.listdir('crawlstocks/task'):
        if each[0] == '_':
            continue
        task.append('crawl_%s' % each.split('.')[0])
    if sys.argv[1] == 'list':
        print("==================================\n")
        for i, each in enumerate(task, 1):
            print('[%d] task: %s' % (i, each))
        print("\n==================================")
    else:
        vdisplay = Xvfb()
        vdisplay.start()
        if sys.argv[1].isdecimal():
            idx = int(sys.argv[1])
            if idx < 1 or idx > len(task):
                print('index [%s] is outside' % idx)
                exit(-1)
            try:
                eval(task[idx-1])()
            except NameError:
                print("not found task: %s" % sys.argv[1])
            except Exception as e:
                print(e)
        elif sys.argv[1].startswith('crawl_'):
            try:
                eval(sys.argv[1])()
            except NameError:
                print("not found task: %s" % sys.argv[1])
            except Exception as e:
                print(e)
        else:
            print('invalid input')
        vdisplay.stop()

