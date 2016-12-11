#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

import requests

import secret

url = 'http://www.tuling123.com/openapi/api'
key = secret.tuling_key


def tuling_chat(fsid, msg):
    r = requests.post(url, data=json.dumps({"key": key, "userid": fsid, "info": msg}))
    return r.json()['text']

if __name__ == '__main__':
    print tuling_chat('11', '你好')