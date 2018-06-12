# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, base64, json

def recognize(image, access_token):
    '''
       返回图片识别结果的字典。
       参数解析：
       -image:str,图片的绝对路径。
       -access_token:str,需要根据百度AI开放平台提供的API Key和Secret Key得到。
                     可以使用tokens中get_token.py中的get_token()方法。
        返回结果的键解释：
        log_id: int,每个结果唯一的id，
        result_num: int,返回结果的数据，即result中元素个数，
        resul: list,返回结果字典的列表，
        +score: float or int, 结果的置信度，范围再0-1，
        +root：识别结果的分类，上层标签，
        +keyword：图片中物体或场景名。
    '''
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