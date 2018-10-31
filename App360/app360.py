#!/usr/bin/env python
# encoding: utf-8
'''
@author: shitian
@file: App360.py
@time: 2018/10/19 10:09
@desc:

'''
import hashlib
import requests
import re
from lxml import etree
import json
import time
import random
import redis
from model import *
from ipproxy import get_proxies_from_redis


def start(page_num):
    global headers
    global i
    global proxies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    start_url = 'http://zhushou.360.cn/list/index/cid/{}?page={}'.format(i, page_num)
    # proxie = get_proxies_from_redis()
    proxies = None#random.choice(proxie)
    # proxies = {'http': random.choice(ip)}
    print(proxies)
    try:
        response = requests.get(start_url, headers=headers, proxies=proxies)
    except:
        print('ip异常')
        start(page_num)
    else:
        print(response.status_code)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            get_url(response.text)


def get_url(page):
    html = etree.HTML(page)
    urls = html.xpath('//*[@id="iconList"]/li/a[1]/@href')
    print(urls)
    for url in urls:
        url = 'http://zhushou.360.cn' + url
        request_detail(url)


def getmd5(hashname):
    """
    哈希处理
    :param hashname:
    :return:
    """
    hashstr=hashlib.md5(hashname.encode("utf-8")).hexdigest()
    return hashstr


def request_detail(url, num=2):
    app = App()
    try:
        # proxie = get_proxies_from_redis()
        # proxies = random.choice(proxie)
        response = requests.get(url, headers=headers, proxies=proxies)
        time.sleep(0.3)
        print(url)
    except:
        request_detail(url, num=2)
    else:
        html = etree.HTML(response.text)
        print(response.status_code)
        if response.status_code == 200:
            try:
                app.app_name = html.xpath('//*[@id="app-name"]/span/text()')[0]
                app.score = html.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[1]/text()')[0]
                app.download_num = html.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[3]/text()')[0]
                app.size = html.xpath('//*[@id="app-info-panel"]/div/dl/dd/div/span[4]/text()')[0]
                tag = html.xpath('/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]/a/text()')
                app.tag = ' '.join(tag)
                app.company = html.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[1]/td[1]/text()')[0]
                app.update_time = html.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[1]/td[2]/text()')[0]
                try:
                    app.version = html.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[2]/td[1]/text()')[0]
                except:
                    app.version = ''
                app.sys = html.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[2]/td[2]/text()')[0]
                app.language = html.xpath('//*[@id="sdesc"]/div/div/table/tbody/tr[3]/td/text()')[0]
                app.crawl_time = datetime.now()
                pattern = re.compile(r"'baike_name': '(.*?)'", re.S)
                aname = re.findall(pattern, response.text)
                app.ahash = getmd5(app.app_name+app.version)
                dbsession = DBSession()
                if i == 1021391:
                    for begin in range(0, 5000, 10):
                        r=get_comment(begin, aname, app.app_name)
                        if r:
                            break
                else:
                    # print('--------------------------------')
                    data = get_data(aname)
                    app.comment = data['mesg']
                    app.best = data['best']
                    app.good = data['good']
                    app.bad = data['bad']
                    if app.tag == '' and num >= 0:
                        request_detail(url, num - 1)
                    else:
                        try:
                            dbsession.add(app)
                            dbsession.commit()
                            print('存储成功！')
                        except:
                            print('已存在！')
            except Exception as e:
                print(e)
        else:
            print('ip被封')


def get_data(aname):
    dic = {
        'baike': aname
    }
    url = 'http://comment.mobilem.360.cn//comment/getLevelCount'
    # proxie = get_proxies_from_redis()
    # proxies = random.choice(proxie)
    try:
        response = requests.get(url, headers=headers, params=dic, proxies=proxies)
    except:
        get_data(aname)
    else:
        data = json.loads(response.text)
        return data


def get_comment(begin, aname, app_name):
    dic = {
        'baike': aname,
        'start': begin
    }
    url = 'http://comment.mobilem.360.cn/comment/getComments'
    try:
        response = requests.get(url, headers=headers, params=dic, proxies=proxies)
        # time.sleep(0.8)
        data = json.loads(response.text)
        # print(data)
    except:
        get_comment(begin, aname, app_name)
    else:
        r=get_comment_detail(data, app_name)
        return r


def get_comment_detail(data, app):
    detail_li = data['data']['messages']
    print(detail_li)
    if not detail_li:
        return True
    dbsession1 = DBSession()
    for detail in detail_li:
        comment = Comment()
        comment.create_time = detail['create_time']
        comment.comment = detail['content']
        comment.user = detail['username']
        comment.type = detail['type']
        comment.app_name = app
        comment.comment_crawl_time = datetime.now()
        print(comment.create_time, comment.comment, comment.user, comment.type, comment.comment_crawl_time)
        dbsession1.add(comment)
    dbsession1.commit()


if __name__ == '__main__':
    i = 12
    for page in range(50, 3000):
        print('第', page, '页')  # 第4页
        start(page)
        if page % 2 == 0:
            print('sleep 20s')
            time.sleep(20)
