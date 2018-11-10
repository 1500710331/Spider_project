#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 15:31
# @Author  : liuyd
# @Site    : 
# @File    : common.py
# @Software: PyCharm

import hashlib
def getmd5(hashname):
    hashstr=hashlib.md5(hashname.encode("utf-8")).hexdigest()
    return hashstr