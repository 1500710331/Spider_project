#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/16 10:06
@Author  : liuyd
@File    : demo.py
@desc    : 
"""



from gevent import monkey
from gevent.pool import Pool

global sum
sum=0
monkey.patch_all()
def info(i):
    global sum
    sum=i


pool=Pool(10)
for i in range(10):
    pool.spawn(info,(i))
pool.join()

print(sum)