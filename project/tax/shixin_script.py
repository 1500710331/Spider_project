# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
import re
import time
import urllib

path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(path, 'shixin_dir')


def response(flow):
    prefix = "https://appv2.qichacha.net/app/v1/legal/shixinSearch"
    """?searchKey=ruan&province=&pageIndex=1&isExactlySame=false&orgType=&cardId=&timestamp=1540627142516&sign=f98c55e8abade32a9336b0c9657911015afe4344"""
    if flow.request.url.startswith(prefix):
        text = str(flow.response.content.decode("utf-8"))
        data_dict = json.loads(text)
        if data_dict.get('message') == '成功':
            url_li = urllib.parse.parse_qsl(flow.request.url)
            search_key = ''
            for t in url_li:
                if 'searchKey' in t[0]:
                    search_key = t[1]
            if search_key:
                filename = os.path.join(dir_path, str(search_key) + "_首页失信查询" + str(time.time()) + ".json")
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(text)

    prefix = "https://appv2.qichacha.net/app/v1/legal/judgmentSearch"
    """?searchKey=%E5%BC%A0%E4%B8%89&province=HB&casetype=&judgeDateBegin=&judgeDateEnd=&pageIndex=1&isExactlySame=false&timestamp=1540782670594&sign=becd4a99b248d743ef90a975eaa0f31213c891d3"""
    if flow.request.url.startswith(prefix):
        text = str(flow.response.content.decode("utf-8"))
        data_dict = json.loads(text)
        if data_dict.get('message') == '成功':
            url_li = urllib.parse.parse_qsl(flow.request.url)
            search_key = ''
            for t in url_li:
                if 'searchKey' in t[0]:
                    search_key = t[1]
            if search_key:
                filename = os.path.join(dir_path, str(search_key) + "_首页裁判文书查询" + str(time.time()) + ".json")
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(text)
