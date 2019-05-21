#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file pub_payload.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-16 15:20:48

import paho.mqtt.client as mqtt
import json
import os
import time

body = """<html><body>
<h2>{}</h2>
<table align='center' cellpadding='10' cellspacing="6">
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}%</td></tr>
    <tr><td>{}</td><td>{}</td></tr>
</table></body></html>"""

body = body.format('大单提醒',
        '股票码', '601992',
        '股票名', '金隅集团',
        '买量率', '55.35',
        '卖量率', '44.65',
        '买距比', '52.40',
        '卖距比', '47.60',
        '买均价', '3.38',
        '卖均价', '3.44',
        '当前价', '3.41',
        '昨收', '3.42',
        '前二买', '20',
        '前二卖', '20',
        '日期', '20190516 09:25:03')

url = 'http://www.xinhuanet.com/politics/leaders/2019-05/16/c_1124502438.htm'

payload1 = {
    'title': '大单提醒测试', 
    'brief': '601992  金隅集团  3.41  3.42  09:25:03',
    'predict': 0,
    'body': body
}

payload2 = {
    'title': '领导新闻提醒测试', 
    'brief': '习大大万岁万岁万万岁',
    'predict': 1,
    'body': url
}

def main():
    data1 = json.dumps(payload1, ensure_ascii=False)
    data2 = json.dumps(payload2, ensure_ascii=False)
    client = mqtt.Client('pub000002')
    client.username_pw_set('stocktech', 'stocktech');
    client.connect(os.environ.get('HOST', '127.0.0.1'), 1883, 60)
    client.publish('/stocktech/reminder/tapereading', data1, qos=0)
    time.sleep(1)
    client.publish('/stocktech/reminder/leadernews', data2, qos=0)
    time.sleep(1)

if __name__ == "__main__":
    main()
