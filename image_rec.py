# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, base64, json

def recognize(image, access_token):
    base_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
    payload = {
        'access_token':access_token,
    }
    header = {
        'Content-Type':'application/x-www.form-urlencoded',
    }
    with open(image, 'br') as f:
        obj = base64.b64encode(f.read())
    resp = requests.post(url=base_url, params=payload, headers=header, data={'image':obj})
    resp.encoding = resp.apparent_encoding
    jsn = resp.text
    dic = json.loads(jsn)
    return dic

if __name__ == '__main__':
    from tokens.get_token import get_token
    access_token = get_token(ak='8oZOs5ypdEPB9cngmlntHX9F',sk='rsH2SpbPitZKVdde6Q44ZxPNY92U47QM')['access_token']
    dic = recognize(r'C:\Users\kkche\Pictures\Saved Pictures\那年那兔那些事儿.jpg',access_token)
    print(dic)