#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/10/18 10:03
@Author  : liuyd
@File    : control_spider.py
@desc    : 
"""

from __future__ import absolute_import, unicode_literals
import traceback
import importlib
import time
import random
from tax.util import log
from tax.util.ipproxy import get_proxies_from_redis
from tax.util.abuyun import get_proxies_from_xun_youzhi2

crawler_map = {
    "shunqi_detail": "enterprise_list.shunqi.shunqi_detail",
    "baidu": "zhixing.baidu_keyword",
    "hei": "zhixing.hei_data",
    "wenshu_data": "wenshu.wenshu_list",
    "wenshu_detail": "wenshu.wenshu_detail",
    "yingyongbao_data": "yingyongbao.get_content_list",
    "yingyongbao_save_details": "yingyongbao.save_app_details",
    "yingyongbao_save_comment": "yingyongbao.save_comment",
    "sougou_content": "sougou.sougou_get_content",
    "sougou_save_data": "sougou.sougou_save_app",
    "wenshu_xingshi_data": "wenshu.wenshu_xingshi_list",
    "wenshu_xingshi_detail": "wenshu.wenshu_xingshi_detail",
    "wenshu_minshi_data": "wenshu.wenshu_minshi_list",
    "wenshu_minshi_detail": "wenshu.wenshu_minshi_detail",
    "wenshu_xingzheng_data": "wenshu.wenshu_xingzheng_list",
    "wenshu_xingzheng_detail": "wenshu.wenshu_xingzheng_detail",
    "wenshu_peichang_data": "wenshu.wenshu_peichang_list",
    "wenshu_peichang_detail": "wenshu.wenshu_peichang_detail",
    "credit_fj_list": "credit_fj.credit_fj_list",
    "credit_fj_detail": "credit_fj.credit_fj_detail"

}


# 代理在这里给
def start(**kwargs):
    """
    :param kwargs: 参数字典必须包含prov键与data键根据prov的值找到对应的脚本代理在这里给
                   data的值为爬虫脚本需要的参数
    :return:
    """
    # 拿代理
    # log.crawler.info("获取的代理数量为:%d"%len(ip_pool))
    is_proxies = kwargs.get("proxies", False)
    module = kwargs.get("module")
    if module is None or module not in crawler_map:
        raise ValueError("请求的modul参数有异常")
    data = kwargs.get("data")
    if data is None or not isinstance(data, dict):
        raise ValueError("请求的modul参数有异常")

    spider_module = importlib.import_module(
        'tax.' + crawler_map[module]
    )
    # 发生异常实现重试3次
    retry = 0
    while retry < 3:
        try:
            if is_proxies:
                ip_pool = get_proxies_from_redis()
                if ip_pool:
                    proxies = random.choice(ip_pool)
                    log.crawler.info(proxies)
                    data['proxies'] = proxies
            result = spider_module.main(**data)
            return result
        except Exception as e:
            time.sleep(random.uniform(1, 2))
            log.crawler.info("发生异常尝试再次连接最多重连3次第{}次连接".format(retry + 1))
            retry += 1
            if retry == 3:
                log.error.info("发生异常,参数为:%s\n,信息为:%s" % (kwargs, traceback.format_exc()))
                raise e
