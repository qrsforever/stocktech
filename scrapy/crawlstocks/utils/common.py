#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

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
            cookies[item['name']] =  item['value']
    except Exception as e:
        print(e)
    return cookies

if __name__ == "__main__":
    # t = cookie_str('/media/lidong/udisk/stocktech/files/gu_qq_cookies.txt')
    # print(t)
    t = cookie_dict('/media/lidong/udisk/stocktech/files/gu_qq_cookies.txt')
    print(t)
