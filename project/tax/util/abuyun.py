#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author  : liuyd
File    : abuyun.py
Theme:
"""
import requests
import platform
import random
import time
import sys
from urllib.parse import urlencode
import logging
import json

ip_list = [
    '123.56.64.235:16819',
    '120.26.167.159:16819',
    '121.42.140.113:16819',
    '121.41.11.179:16819',
    '117.48.201.187:16819',
    '180.76.154.18:16819',
    '123.56.144.1:16819',
    '120.27.218.32:16819',
    '114.215.140.117:16819',
    '120.76.142.46:16819',
    '122.114.82.64:16819',
    '114.215.140.117:16819',
    '116.62.128.50:16819',
    '114.67.228.126:16819',
    '115.28.102.240:16819',
    '117.48.201.187:16819',
    '121.41.11.179:16819',
    '121.42.140.113:16819',
    '123.57.67.124:16819',
    '43.226.164.156:16819'
]


def get_abuyun_proxies():
    # ! -*- encoding:utf-8 -*-

    import requests

    # 要访问的目标页面
    targetUrl = "http://test.abuyun.com/proxy.php"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H46739XT407HL60D"
    proxyPass = "D0FC348E32EB7E96"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

def get_abuyun_proxies_zhuanyeban():
    import requests

    # 要访问的目标页面
    targetUrl = "http://proxy.abuyun.com/current-ip"
    # targetUrl = "http://proxy.abuyun.com/switch-ip"
    # targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器
    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "H8997N5W1E698P5P"
    proxyPass = "DD01C183CE12BC99"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    resp = requests.get(targetUrl, proxies=proxies)
    return proxies,resp.text


    url='http://httpbin.org/ip'
    r=requests.get(url=url,proxies=proxies)
    print(r.status_code)
    print(r.text)

def get_proxies_from_kuaisimi():
    proxy=random.choice(ip_list)
    proxy="http://{ip}".format(ip=proxy)
    proxies={"http":proxy,"https":proxy}
    return proxies

def check_proxy(proxies):
    fips=[]
    url="http://www.moguproxy.com/proxy/checkIp/ipList?"
    params=""
    for ip in proxies:
        testip=ip['ip']+":"+ip["port"]
        p=urlencode({"ip_ports[]":testip})
        params+=p+"&"
    params=params[:-1]
    url=url+params
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host':'www.moguproxy.com'
    }
    res=requests.get(url=url)
    content=res.text
    jsonA=json.loads(content)
    if jsonA:
        ips_list=jsonA['msg']
        for ip in ips_list:
            xtime=ip.get('time',None)
            if xtime:
                s=xtime.split('ms')[0]
                if int(s)<=200:
                    ip="http://"+ip['ip']+":"+ip["port"]
                    pip={"http":ip,"https":ip}
                    fips.append(pip)
                else:
                    continue
            else:
                continue
    return fips




def get_proxies_from_mogu():
    url="http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=b4b3b100088d4ec6afc3c6f1baf60b26&count=30&expiryDate=0&format=1&newLine=2"
    res=requests.get(url=url)
    jsondata=json.loads(res.text)
    ip_pool=jsondata['msg']
    proxies=check_proxy(ip_pool)
    if proxies:
        return proxies

def get_proxies_from_xun():
    url="http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD201810175939w4ijrM/ac0afef7033e11e7942200163e1a31c0?returnType=2"
    res=requests.get(url=url)
    jsondata = json.loads(res.text)
    ip=jsondata['RESULT']
    if ip:
        host=ip["wanIp"]
        port=ip["proxyport"]
        proxy="http://"+host+":"+port
        print(proxy)
        proxies={"https":proxy,"http":proxy}
        return proxies

def get_proxies_from_xun_youzhi():
    ip_pool=[]
    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=bee3b5cbacef42f89f861130ed898e71&orderno=YZ201810192048oyA1Wm&returnType=2&count=5"
    res = requests.get(url=url)
    jsondata = json.loads(res.text)
    ips = jsondata['RESULT']
    print(ips)
    if ips:
        for ip in ips:
            host = ip["ip"]
            port = ip["port"]
            proxy = "http://" + host + ":" + port
            proxies = {"https": proxy, "http": proxy}
            ip_pool.append(proxies)
    return ip_pool

def get_proxies_from_xun_youzhi2():
    ip_pool = []
    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=6c2cf39c53c94c61b8f88f8b5b7e3048&orderno=YZ2018101881947r1INj&returnType=2&count=2"
    res = requests.get(url=url)
    jsondata = json.loads(res.text)
    ips = jsondata['RESULT']
    if ips:
        for ip in ips:
            host = ip["ip"]
            port = ip["port"]
            proxy = "http://" + host + ":" + port
            proxies = {"https": proxy, "http": proxy}
            ip_pool.append(proxies)
    return ip_pool




def get_proxies_from_sun():
    """
    提取太阳代理的函数
    :return:
    """
    ip_pool = []
    url ="http://http.tiqu.qingjuhe.cn/getip?num=5&type=2&pro=0&city=0&yys=0&port=1&pack=22832&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=0&regions="
    res = requests.get(url=url)
    jsondata = json.loads(res.text)
    # if jsondata["success"]=="true":
    #     print("提取太阳代理成功!!!")
    ips = jsondata['data']
    if ips:
        for ip in ips:
            host = ip["ip"]
            port = ip["port"]
            proxy = "http://" + host + ":" + port
            proxies = {"https": proxy, "http": proxy}
            ip_pool.append(proxies)
        return ip_pool





if __name__=="__main__":
    data={'code': 0, 'success': True, 'msg': '0',
     'data': [{'ip': '222.220.111.182', 'port': '4378'}, {'ip': '222.220.64.171', 'port': '4384'},
              {'ip': '117.57.36.248', 'port': '4373'}, {'ip': '175.42.158.127', 'port': '4354'},
              {'ip': '220.164.227.162', 'port': '4335'}]}
    print(data['success'])
