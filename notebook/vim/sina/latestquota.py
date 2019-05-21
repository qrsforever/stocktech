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
        '$lte': datetime(2019, 5, 20, 15, 1, 0), 
        }},
    {'_id': 0} # 过滤掉_id域
    )))

# 显示所有列名
print(data.columns)

# 前5项
data[['name', 'code', 'high', 'low', 'open', 'price', 'datetime']].head(5)

# 后5项
data[['name', 'code', 'b_p', 'a_p', 'datetime']][-5:]


#####################################################################################
# <codecell>
#####################################################################################
plt.figure(figsize=(20,10))
type(data['price'][0:100])
plt.plot(data['price'][0:100])
plt.show()
