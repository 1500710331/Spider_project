# -*- coding: utf-8 -*-
"""
@function:使用requests请求代理服务器,请求http适用网页适用，不适用请求https网页
@author:xuzy
"""

from gevent import monkey
from gevent.pool import Pool
from urllib.parse import urlparse
import threading
import platform
import requests
import time
import base64
import random
import random
import redis
import ast


pl=platform.system()

if pl=="Linux":
    redis_obj=redis.Redis(host='172.17.98.1',port=6379,db=4)
else:
    redis_obj = redis.Redis(host='master', port=6379,db=4,password='ding')

global stotal
global ftotal
stotal=0
ftotal=0
fips=[]


def get_proxy():
    # 要访问的目标网页
    page_url = "http://dev.kuaidaili.com/testproxy"

    # 代理服务器
    proxy = ['122.114.82.64:16819',
             '114.215.140.117:16819',
             '116.62.128.50:16819',
             '114.67.228.126:16819',
             '115.28.102.240:16819',
             '117.48.201.187:16819',
             '121.41.11.179:16819',
             '121.42.140.113:16819',
             '123.57.67.124:16819',
             '43.226.164.156:16819',
             ]

    # 用户名和密码(私密代理/独享代理)
    username = "zhangqm"
    password = "z23lb6t1"
    ip=random.choice(proxy)
    proxies = {'http': 'http://zhangqm:z23lb6t1@%s' %ip,"https:":'http://zhangqm:z23lb6t1@%s' % ip }
    print('正在使用代理:{}'.format(proxies))

    return proxies



def get_proxy_from_kuaidaili():
    url = 'http://ent.kdlapi.com/api/getproxy/?orderid=932948560315953&num=500&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol' \
          '=1&method=1&an_ha=1&sp1=1&quality=1&sort=1&format=json&sep=1'
    print(url)
    response = requests.get(url)
    return response.json()['data']['proxy_list']


def check_kuai_proxy(proxies):
    url='http://zxgk.court.gov.cn/zhixing/new_index.html'
    r = urlparse(url)
    host = r.netloc
    headers.update(host=host)
    try:
        response = requests.get(url=url,proxies=proxies,headers=headers,timeout=20)
        if response.status_code==200:
            redis_obj.sadd(proxies,proxies)
            redis_obj.expire(proxies,200)
            log.crawler.info(threading.current_thread().name+" is success")
            global stotal
            stotal+=1

        else:
            log.crawler.info(threading.current_thread().name + " is failure")
            global ftotal
            ftotal+=1
    except Exception as e:
        print(e)
        # fips.append(1)



def get_one_proxeis_from_redis():
    pass


def get_proxies_from_redis():
    ip_pool = []
    keys_list = redis_obj.keys()
    if keys_list:
        for k in keys_list:
            ex = redis_obj.ttl(k)
            try:
                if ex > 30:
                    proxy = k.decode()
                    proxy = ast.literal_eval(proxy)
                    ip_pool.append(proxy)
            except:
                continue
        if ip_pool:
            print("proxies pool length is:%d"%len(ip_pool))
            return ip_pool
        else:
            time.sleep(10)
            print("所有代理的过期时间小于60秒将继续拉代理")
            return get_proxies_from_redis()
    else:
        print("代理提取发生阻塞将sleep 10秒再提取......")
        time.sleep(10)
        return get_proxies_from_redis()


def fetch_proxies_to_redis():
    st=time.time()
    proxies_list=[]
    threads = []
    ips = get_proxy_from_kuaidaili()
    print(ips)
    total=len(ips)
    while True:
        for t1 in threads:
            if not t1.is_alive():
                threads.remove(t1)
        log.crawler.info("threads len :%d ips len :%d"%(len(threads),len(ips)))
        if len(threads)>=10:
            time.sleep(3)
            continue
        index=len(ips)-1
        if ips:
            p=ips.pop()
            proxy = 'http://' + p
            proxies = {'https': proxy, 'http': proxy}
            t=threading.Thread(target=check_kuai_proxy,args=(proxies,),name="thread_proxies_"+str(index))
            t.setDaemon(True)
            t.start()
            threads.append(t)
        else:
            break
    log.crawler.info("the finally threads length is:%d"%len(threads))
    for t in threads:
        t.join()
    et = time.time()
    log.crawler.info("total is:%d,success is:%d,failure is:%d"%(total,stotal,ftotal+len(fips)))
    return proxies_list


def startproxies():
    while True:
        st = time.time()
        fetch_proxies_to_redis()
        en = time.time()
        print("cost is:%s" % (en - st))
        time.sleep(10)


if __name__ == '__main__':
    ips=get_proxies_from_redis()
    print(ips)


