#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import datetime

def zone_code(code):
    if code[0] in ['0','2','3']:
        code='sz'+code
    elif code[0] in ['6','9']:
        code='sh'+code
    else:
        pass
    return code

def cookie_str(cookiefile):
    try:
        cookies = []
        with open(cookiefile, 'r', encoding='utf-8') as f:
            cookies = json.loads(f.read())
        ll = [item['name'] + "=" + item['value'] for item in cookies]
        return '; '.join(ll)
    except:
       return None

def cookie_dict(cookiefile):
    cookies = dict()
    try:
        listcookies = []
        with open(cookiefile, 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())
        for item in listcookies:
            cookies[item['name']] = item['value']
    except Exception as e:
        print(e)
    return cookies

def get_every_days(begin, end, flag = 1, fmt='%Y%m%d'):
    # flag = 0: all days, flag = 1: workdays, flag = 2: weakend days
    # days = []
    if isinstance(begin, str):
        begin = datetime.datetime.strptime(begin, fmt)
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, fmt)
    while begin <= end:
        if flag == 1:
            if begin.weekday() <= 4:
                yield begin.strftime(fmt)
                # days.append(begin.strftime(fmt))
        elif flag == 2:
            if begin.weekday() >= 5:
                # days.append(begin.strftime(fmt))
                yield begin.strftime(fmt)
        else:
            # days.append(begin.strftime(fmt))
            yield begin.strftime(fmt)

        begin += datetime.timedelta(days=1)
    # return days

if __name__ == "__main__":
    # print(cookie_str('/media/lidong/udisk/stocktech/files/gu_qq_cookies.txt'))
    # print(cookie_dict('/media/lidong/udisk/stocktech/files/gu_qq_cookies.txt'))
    days = get_every_days('20190301', datetime.datetime.now(), 2)
    for day in days:
        print(day)
