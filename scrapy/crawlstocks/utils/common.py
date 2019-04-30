#!/usr/bin/python3
# -*- coding: utf-8 -*-

def zone_code(code):
    if code[0] in ['0','2','3']:
        code='sz'+code
    elif code[0] in ['6','9']:
        code='sh'+code
    else:
        pass
    return code

def trans_cookie(cookie):
    item_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        item_dict[key] = value
    return item_dict
