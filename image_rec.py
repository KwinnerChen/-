# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, base64, json

def recognize(image, access_token, flag=1):
    '''
       返回图片识别结果的字典。
       参数解析：
       -image:str,图片的绝对路径。
       -access_token:str,需要根据百度AI开放平台提供的API Key和Secret Key得到。
                     可以使用tokens中get_token.py中的get_token()方法。
       -flag: 1 or 2, 与access_token对应，当access_token为检测类型时为1，检测内容时为2.

        返回结果的键解释：
        log_id: int,每个结果唯一的id，
        result_num: int,返回结果的数据，即result中元素个数，
        resul: list,返回结果字典的列表，
        +score: float or int, 结果的置信度，范围再0-1，
        +root：识别结果的分类，上层标签，
        +keyword：图片中物体或场景名。
    '''
    base_url_1 = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
    base_url_2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
    payload = {
        'access_token':access_token,
    }
    header = {
        'Content-Type':'application/x-www.form-urlencoded',
    }
    with open(image, 'br') as f:
        obj = base64.b64encode(f.read())
    if flag == 1:
        resp = requests.post(url=base_url_1, params=payload, headers=header, data={'image':obj})
    elif flag == 2:
        resp = requests.post(url=base_url_2, params=payload, headers=header, data={'image':obj})
    resp.encoding = resp.apparent_encoding
    jsn = resp.text
    dic = json.loads(jsn)
    return dic

if __name__ == '__main__':
    from tokens.get_token import get_token
    access_token = get_token(ak='hgO2AIK9L5s20coavGHBRyQI',sk='gK5AQOzUgtirD4EPlSlbuRscbKVnWZMU')['access_token']
    dic = recognize(r'C:\Users\kkche\Pictures\003bsgbmgy6R6efoOr1c3.png',access_token, flag=2)
    print(dic)