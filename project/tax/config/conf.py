#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/9 14:17
@Author  : liuyd
@File    : conf.py
@desc    : 
"""
import os
from yaml import load
config_path=os.path.join(os.path.dirname(__file__),'crawler.yaml')


with open(config_path,encoding='utf-8') as f:
    content=f.read()
cf=load(content)



def get_proxies_api(name):
    return cf.get(name)
