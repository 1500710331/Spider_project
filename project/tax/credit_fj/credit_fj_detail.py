#!/usr/bin/env python
# encoding: utf-8
'''
@author: shitian
@file: credit_fj_detail.py
@time: 2018/11/9 15:32
@desc:

'''

from lxml import etree
import hashlib
import requests
from tax.model.handle_redis import HandleRedis, RedisPool
from tax.util import log
from tax.util.headers import headers


def get_detail(**kwargs):
    proxies = kwargs.get('proxies', None)
    url = kwargs.get('url')
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        parse(response.text)


def parse(response):
    item = dict()
    person_li = []
    enterprise_li = []
    result = etree.HTML(response)
    item["PNAME"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[1]/td/text()')[0].strip()
    item["CASE_CODE"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[2]/td/text()')[0].strip()
    item["FACTS"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[4]/td/text()')[0].strip()
    item["AM_HASH"] = getmd5(item["CASE_CODE"]+item["PNAME"])
    item["AGE"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[5]/td/text()')[0].strip()
    item["COURT_NAME"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[6]/td/text()')[0].strip()
    item["EXEC_CODE"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[7]/td/text()')[0].strip()
    item["LAW_NAME"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[8]/td/text()')[0].strip()
    item["PUBLISH_TIME"] = result.xpath('/html/body/div/main/div/div/div/div/div/div/div/table/tr[9]/td/text()')[0].strip()
    item["DATA_SOURCE"] = 'http://www.fjcredit.gov.cn/creditsearch.redlist.dhtml?source_id=100'
    if item["AGE"] == '0':
        item.pop('AGE')
        person_li.append(item)
        hr.cache_list_redis("TB_SHIXIN_ENTERPRISE", person_li)
    else:
        item.pop('LAW_NAME')
        enterprise_li.append(item)
        hr.cache_list_redis("TB_SHIXIN_PERSON", enterprise_li)


def getmd5(hashname):
    """
    哈希处理
    :param hashname:
    :return:
    """
    hashstr=hashlib.md5(hashname.encode("utf-8")).hexdigest()
    return hashstr


def main():
    global hr
    hr = HandleRedis(7)
    while True:
        url = hr.get_data_redis("TB_CREDIT_FJ_URL")
        if url:
            kwargs = dict(url=url)
            get_detail(**kwargs)


if __name__ == '__main__':
    main()
