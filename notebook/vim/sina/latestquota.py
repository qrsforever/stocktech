#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file latestquota.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-17 21:28:18

### Run the file using jupyter-vim ###

from pymongo import MongoClient

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

file_tmp_png = '/tmp/jupyter_vim.png'

# %alias vim.show eog $file_tmp_png
def vim_show():
    # %vim.show
    # %system eog $file_tmp_png
    pass

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
latestquota = client.stocktech.latestquota

latestquota.find_one()

#####################################################################################
# <codecell> 读取数据并显示
#####################################################################################
data = pd.DataFrame(list(latestquota.find(
    {'datetime': {
        '$gte': datetime(2019, 5, 20, 9, 0, 0),  # 查询时间范围
        '$lte': datetime(2019, 5, 20, 11, 30, 0),
        }},
    {'_id': 0} # 过滤掉_id域
    )))

# 显示所有列名
print(data.columns)

# 前5项
data[['name', 'code', 'high', 'low', 'open', 'price', 'datetime']].head(5)

# 后5项
data[['name', 'code', 'b_p', 'a_p', 'datetime']][-5:]

# 过滤

#####################################################################################
# <codecell> 拉夏贝尔
#####################################################################################
data_groupby_code = data.groupby(by='code')
data_laxia = data_groupby_code.get_group('603157')
# 获取昨日收盘价
settlement = data_laxia.iloc[0].at['settlement']
# 选取有用的列名
data_laxia = data_laxia[['name', 'code', 'datetime', 'price', 'b_p', 'a_p']]
# 设置日期为行索引
data_laxia = data_laxia.set_index('datetime')
# 标签重命名
data_laxia.rename(columns={
    'name':'股票名',
    'code':'股票码',
    'price':'当前价',
    'b_p': '竞买价',
    'a_p': '竟卖价',
    }, inplace=True)
data_laxia.head(5)

#####################################################################################
# <codecell> 显示 "当前价", "竞买价", "竞买价"
#####################################################################################
highest = round(settlement * 1.10, 2)
lowest = round(settlement * 0.9, 2)
data_laxia.plot(figsize=(30, 20), grid=True, style='-', rot=45,
        ylim=[lowest, highest], subplots=True, title=u'价格变化')
plt.savefig(file_tmp_png)
