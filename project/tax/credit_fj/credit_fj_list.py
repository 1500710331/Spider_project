#!/usr/bin/env python
# encoding: utf-8
'''
@author: shitian
@file: credit_fj_list.py
@time: 2018/11/9 14:34
@desc:

'''

import requests
from tax.util.headers import headers
from lxml import etree
from tax.model.handle_redis import HandleRedis, RedisPool
from tax.util import log


def get_page(**kwargs):
    hr = HandleRedis(7)
    proxies = kwargs.get("proxies", None)
    keyword = kwargs.get('keyword')
    for page in range(1, 101):
        url = 'http://www.fjcredit.gov.cn/creditsearch.redlist.dhtml?source_id=100&kw={}&page={}'.format(keyword, page)
        response = requests.get(url, headers=headers, proxies=proxies)
        response.encoding = response.apparent_encoding
        kwargs = dict(response=response.text, hr=hr)
        get_detail(**kwargs)


def get_detail(**kwargs):
    hr = kwargs.get('hr')
    s = kwargs.get('response')
    result = etree.HTML(s)
    urls = result.xpath('/html/body/div/main/div/div/div/div/div/div[2]/div/div[2]/table/tr/td[1]/a/@href')
    all_url = []
    for url in urls:
        url = 'http://www.fjcredit.gov.cn' + url
        all_url.append(url)
    if all_url:
        hr.cache_list_redis('TB_CREDIT_FJ_URL', all_url)
        log.crawler.info("cache fj_url into redis success length is:%s" % len(all_url))


def main(**kwargs):
    get_page(**kwargs)


if __name__ == '__main__':
    kwargs = dict(keyword='干')
    main(**kwargs)
