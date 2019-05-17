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

#####################################################################################
# <codecell> Connect db
#####################################################################################

client = MongoClient('localhost', 27027)
latestquota = client.stocktech.latestquota

latestquota.find_one()

#####################################################################################
# <codecell>
#####################################################################################
# data = pd.DataFrame(list(
data = latestquota.find(
    {'datetime': {'$lt': datetime(2019, 5, 17)}},
    {'_id': 0}
    ) #))

data = list(data)
data[0]
len(data)
data[199755]
