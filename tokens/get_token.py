# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import pickle, json
import time

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_token_%s.txt')

def _refresh_token(ak, sk):  # 请求token，返回字典
    '''ak:API_Key,
       sk:Secret_Key,
    '''
    base_url = 'https://aip.baidubce.com/oauth/2.0/token'
    payload = {
        'grant_type':'client_credentials',
        'client_id':ak,
        'client_secret':sk,
    }
    header = {
        'Content-Type':'application/json; charset=UTF-8',
    }
    resp = requests.post(url=base_url, params=payload, headers=header)
    jsn = resp.text
    dic = json.loads(jsn)
    dic.update({'client_id':ak, 'client_secret':sk})
    return dic

def get_token(ak, sk, flag='content'):  # 试图从文件读取token，过期或不存在或密钥不匹配刷新后，再返回字典
    '''用于获取ak=api_key,sk=secret_key的token，返回的是一个字典。ak,sk在百度开放AI平台账户生成。
       包含:
       "refresh_token":str,
       "expires_in":int，有效时间，秒，
       "scope":str,
       "session_key":str,
       "access_token:str,用于api,
       "session_secret":str
       "flag":str,token的用途，用于识别类型时为“type”，用于识别内容是为“content”。
       '''
    file = file_path % flag
    if os.path.isfile(file) and os.path.getsize(file)>0:
        with open(file, '+rb') as f:
            dic = pickle.load(f)
            if dic['client_id'] != ak or dic['client_secret'] != sk:
                dic = _refresh_token(ak, sk)
                pickle.dump(dic, f)
                return dic
            elif time.time()-os.path.getatime(file) > dic.get('expires_in'):
                dic = _refresh_token(ak, sk)
                pickle.dump(dic, f)
                return dic         
            else:
                return dic
    else:
        dic = _refresh_token(ak, sk)
        with open(file, 'wb') as f:
            pickle.dump(dic, f)
        return dic

if __name__ == '__main__':
    dic = get_token(ak='hgO2AIK9L5s20coavGHBRyQI', sk='gK5AQOzUgtirD4EPlSlbuRscbKVnWZMU')
    print(dic['access_token'])