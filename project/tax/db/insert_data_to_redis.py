#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/19 15:44
@Author  : liuyd
@File    : insert_data_to_redis.py
@desc    : 
"""
import sys
import platform
import redis
pl=platform.system()

if pl=="Linux":
    redis_obj=redis.Redis(host='172.17.98.1',port=6379,db=1)
else:
    redis_obj = redis.Redis(host='master', port=6379,db=1,password='ding')

def start(file):
    file=open(file,"r",encoding="utf-8")
    content=file.read()
    lines=content.split("\n")
    words=list(set(lines))
    print(len(words))
    wfile="shixin_court_words"
    redis_obj.sadd(wfile,*words)

if __name__=='__main__':
    file="court_shixin_words.txt"
    start(file)
