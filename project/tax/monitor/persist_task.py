#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/9 14:06
@Author  : liuyd
@File    : persist_task.py
@desc    : 从redis里取数据存入mysql
"""
import ast
from tax.config.conf import *
from tax.PublicSpider.get_content_static import log,HandDb,DbHandle
from tax.model.handle_redis import HandleRedis
from tax.PublicSpider.common import getmd5

hr=HandleRedis(7)
db=DbHandle()


def persis_data_into_mysql(table,datas):
    hd=HandDb(table)
    for data in datas:
        sql=hd.generate_sql_dict(data)
        db.insert_db_func(sql=sql)

def get_result_data(table):
    keys_name=table
    pop_data_list = []
    # 定义一个列表用来保存反馈的数据
    feedback_data_list = []
    # 一次最大传递数据量
    once_num = 100
    nums = hr.get_length(keys_name)
    if nums:
        log.crawler.info("keys name:%s 数据量为:%d"%(keys_name,nums))
        for i in range(min(nums,once_num)):
            res = hr.get_data_redis(keys_name)
            if res:
                data = ast.literal_eval(res)
                if table=="tb_credit":
                    data['credit_level']='A'
                elif table=="TB_SHIXIN_PERSON" or table=="TB_SHIXIN_ENTERPRISE":
                    hashstr=data.get("CASE_CODE","")+data.get("PNAME","")
                    hashvalue=getmd5(hashstr)
                    data["AM_HASH"]=hashvalue
                pop_data_list.append(data)
            else:
                break
        return pop_data_list
    else:
        log.crawler.info(("keys name:%s 数据为空"%keys_name))

def run(table):
    datas=get_result_data(table)
    if datas:
        persis_data_into_mysql(table,datas)




