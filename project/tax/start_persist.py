#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/18 13:49
@Author  : liuyd
@File    : start_persist.py
@desc    : 对数据进行持久化的模块,逻辑是从redis里取代理存储到mysql
"""
import time
from tax.monitor.persist_task import run
from tax.util import log

# table_list=["TB_SHIXIN_ENTERPRISE","TB_SHIXIN_PERSON","TB_WENSHU_ZHIXING","sougou_app","yingyongbao_app","comment_yingyongbao"]
table_list = ["sougou_app","yingyongbao_app","comment_yingyongbao"]
while True:
    for table in table_list:
        log.crawler.info("start persist table is:%s"%table)
        run(table)
        time.sleep(0.5)
    # continue


