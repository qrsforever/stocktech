#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file chddata.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-22 21:16:04

### Run the file using jupyter-vim ###

from pymongo import MongoClient

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

file_tmp_png = '/tmp/jupyter_vim.png'

#####################################################################################
# <codecell> 全局配置
#####################################################################################
# 中文
plt.rcParams['font.sans-serif'] = 'SimHei'
# 负号正常显示
plt.rcParams['axes.unicode_minus'] = False

#####################################################################################
# <codecell> 连接数据库
#####################################################################################
client = MongoClient('localhost', 27027)
chdata = client.stocktech.chddata

chdata.find_one()

#####################################################################################
# <codecell> 201805-201905数据
#####################################################################################
data = pd.DataFrame(list(chdata.find(
    {'date': {
        '$gte': datetime(2018, 5, 1, 0, 0, 0),
        '$lte': datetime(2019, 5, 1, 0, 0, 0),
        }, 'code': '603157'},
    {'_id': 0, 'code': 1, 'name': 1, 'tclose': 1, 'date':1}
    )))

#####################################################################################
# <codecell> 画图
#####################################################################################
data = data.set_index('date')
data['5d'] = data['tclose'].rolling(window=5).mean()
data['10d'] = data['tclose'].rolling(window=10).mean()
data['20d'] = data['tclose'].rolling(window=20).mean()
data[['tclose', '5d', '10d', '20d']].plot(figsize=(20, 10), grid=True)
plt.savefig(file_tmp_png)

#####################################################################################
# <codecell> 5日差, 10日差
#####################################################################################
data['5d-10d'] = data['5d'] - data['10d']
data['5d-20d'] = data['5d'] - data['20d']
data[['tclose', '5d-10d', '5d-20d']].plot(figsize=(20, 10),
        style='b', subplots=True, grid=True)
plt.savefig(file_tmp_png)
