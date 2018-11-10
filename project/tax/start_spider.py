#!/usr/bin/env python
# encoding: utf-8
'''
@author: liuyd
@file: start_spider.py
@time: 2018/8/8 16:33
@desc:
'''
import time
from tax.monitor.tasks import baidu_shixin,start_hei,start_wenshu,start_shunqi_detail,start_sougou,start_yingyongbao,start_wenshu_xingshi,start_wenshu_minshi,start_wenshu_xingzheng,start_wenshu_peichang
from tax.zhixing.shixin_zhixing import start_court

while True:
    try:
        #start_wenshu_minshi()
        #start_wenshu_xingzheng()
        #start_wenshu_peichang()
        start_wenshu_xingshi()
        # start_yingyongbao()
        # start_sougou()
        # start_court()
        # start_shunqi_detail()
        #start_wenshu()
        # start_anhui_task()
        # start_hei()
        # start_wenshu()
        # start()
        # time.sleep(5)
    except Exception as err:
        continue




