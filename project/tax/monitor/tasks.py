#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 15:59
# @Author  : liuyd
# @Site    : 
# @File    : tasks.py
# @Software: PyCharm
import time
from gevent import monkey
import threading
from gevent.pool import Pool
import ast
from tax.monitor.save_mysql import Mysql
from tax.util import log
from tax.control_spider import start
from tax.model.handle_redis import HandleRedis, RedisPool
import multiprocessing

hr = HandleRedis(1)


def enterprise_list(**kwargs):
    k = kwargs.get("k", None)
    if not k:
        raise ValueError("k 参数存在错误......")
    item = hr.get_data_redis(k)
    if item:
        url = item
        item = ast.literal_eval(item)
        if isinstance(item, dict):
            url = item['url']
        city = item['city']
        prov = item['prov']
        log.crawler.info("start crawler prov:%s,city:%s,url is:%s" % (prov, city, url))
        module = "shunqi_list"
        kwargs = dict(module=module, data={"url": url, "city": city, "prov": prov})
        try:
            start(**kwargs)
        except Exception as err:
            k = "shunqi_detail"
            log.crawler.info("顺企网详细页面爬取发生异常将参数缓存到原来的key")
            hr.put_str_into_redis(k, item)


def get_detail_info(**kwargs):
    monkey.patch_all()
    pool = Pool(10)
    for i in range(10):
        kwargs = dict(id=i)
        pool.spawn(multhread_shunqidetail, **kwargs)
    pool.join()


def multhread_shunqidetail(**kwargs):
    gid = kwargs.get("id")
    log.crawler.info("gevent is start id is:%d" % gid)
    k = "shunqi_detail"
    item = hr.get_data_redis(k)
    if item:
        url = item
        item = ast.literal_eval(item)
        if isinstance(item, dict):
            url = item['url']
        city = item['city']
        prov = item['prov']
        log.crawler.info("start crawler prov:%s,city:%s,url is:%s" % (prov, city, url))
        module = k
        kwargs = dict(module=module, data={"url": url, "city": city, "prov": prov})
        try:
            start(**kwargs)
            log.crawler.info("the gevent is finished id is:%d" % gid)
        except Exception as err:
            k = "shunqi_detail"
            log.crawler.info("顺企网详细页面爬取发生异常将参数缓存到原来的key")
            hr.put_str_into_redis(k, item)
            raise err


def get_detail_url(**kwargs):
    k = "shunqi_list"
    item = hr.get_data_redis(k)
    print(item)
    total = None
    if item:
        url = item
        item = ast.literal_eval(item)
        if isinstance(item, dict):
            url = item['url']
        city = item['city']
        prov = item['prov']
        log.crawler.info("start crawler prov:%s,city:%s,url is:%s" % (prov, city, url))
        module = k
        kwargs = dict(module=module, data={"url": url, "city": city, "prov": prov})
        try:
            total = start(**kwargs)
            log.crawler.info("total num is:%s" % total)
        except Exception as e:
            log.crawler.info("顺企网首页请求发生异常将参数缓存到原来的key")
            k = "shunqi_list"
            hr.put_str_into_redis(k, item)
        if total:
            if not isinstance(total, int):
                total = int(total)
            for i in range(2, total + 1):
                try:
                    log.crawler.info("start crawler url is:%s,page is:%s" % (url, i))
                    kwargs = dict(module=module, data={"url": url, "city": city, 'page': i, "prov": prov})
                    start(**kwargs)
                except Exception as e:
                    log.crawler.info("发生异常将URL缓存到redis......")
                    url = url.format(page=i)
                    data = dict(city=city, url=url, prov=prov)
                    k = "shunqi_list_error"
                    hr.put_str_into_redis(k, data)


def baidu_shixin(**kwargs):
    """
       定时任务调用失信爬虫百度失信的爬取策略
       :return:
       """
    # ip_pool=get_proxies_from_redis()
    r = HandleRedis(1)
    name = r.get_data_redis("shixin_words")
    # flag为一个开关确定是否需要重新遍历关键词
    # flag = r.get('baidushixin_flag')

    data = {}
    if name:
        name = name
    else:
        log.crawler.info('百度失信关键词遍历完毕.....')
        return
    try:
        pn = 0
        hr = HandleRedis(7)
        while isinstance(pn, int):
            kwargs = dict(module='baidu', data=dict(name=name, pn=pn))
            # if ip_pool:
            #     proxies = random.choice(ip_pool)
            # else:
            #     ip_pool = get_proxies_from_redis()
            #     proxies = ip_pool.pop()
            # kwargs['data']['proxies'] = proxies
            log.crawler.info("crawler name is:{},pn is:{}".format(name, pn))
            result_dict = start(**kwargs)
            qiye = result_dict['enterprise']
            person = result_dict['person']
            if qiye:
                hr.cache_list_redis('TB_SHIXIN_ENTERPRISE', qiye)
                log.crawler.info("cache qiye shixin into redis success length is:%s" % len(qiye))
            if person:
                hr.cache_list_redis('TB_SHIXIN_PERSON', person)
                log.crawler.info("cache person shixin into redis success length is:%s" % len(person))
            pn = result_dict["pn"]
            if pn == "finished":
                log.crawler.info("数据请求完毕name:{},pn:{}".format(name, pn))
                break
            elif pn == 2000:
                break
            else:
                pn += 10
    except Exception as err:
        log.error.info('百度失信爬虫发生异常,信息为:\n%s' % err)


def start_hei():
    r = RedisPool(client_db=1)
    rp = r.redis_pool()
    page = rp.get("hei_page")
    if not page:
        rp.set("hei_page", 1)
        page = 1
    else:
        page = int(page.decode())
    log.crawler.info("start hei shixin page is:%d" % page)
    rp.incrby("hei_page", 1)
    kwargs = dict(module="hei", data=dict(page=page))
    start(**kwargs)


def start_wenshu(**kwargs):
    r = HandleRedis(1)
    name = r.get_data_redis("wenshu_keys")
    if name:
        name = name
        print(name)
    else:
        log.crawler.info('裁判文书关键词遍历完毕.....')
        return
    index = 1
    while True:
        log.crawler.info("*" * 80)
        log.crawler.info("start crawler wenshu page is:%d" % index)
        kwargs = dict(module="wenshu_data", data=dict(key=name, index=index), proxies=True)
        items = start(**kwargs)
        log.crawler.info("获取的文件ID长度为:%d" % (len(items) - 1))
        if len(items) == 1:
            break
        if items:
            run_eval = items[0]['RunEval']
        else:
            break
        # monkey.patch_all()
        # pool = Pool(20)
        threads = []
        for item in items[1:]:
            if threads:
                for t1 in threads:
                    if not t1.is_alive():
                        threads.remove(t1)
            if len(threads) == 10:
                time.sleep(3)
                continue
            data = {}
            data["docid"] = item["文书ID"]
            data["CASE_TYPE"] = item["案件类型"]
            data["CASE_TIME"] = item["裁判日期"]
            data["CASE_NAME"] = item["案件名称"]
            data["CASE_NUM"] = item["案号"]
            data["COURT_NAME"] = item["法院名称"]
            data['runeval'] = run_eval
            d = dict(module="wenshu_detail", data=data, proxies=True)
            t = threading.Thread(target=start, kwargs=d, name=None)
            t.setDaemon(True)
            t.start()
            t.join()
        for t in threads:
            t.join()
        index += 1


# def start_anhui_task(**kwargs):
#     r = RedisPool(client_db=1)
#     rp = r.redis_pool()
#     page = rp.get("anhui_page")
#     if not page:
#         rp.set("anhui_page", 1)
#         page = 1
#     else:
#         page = int(page.decode())
#     rp.incrby("anhui_page", 1)
#     start_anhui(page=page)
#     log.crawler.info("start anhui shixing page is:%d" % page)

def start_shunqi_detail(**kwargs):
    get_detail_info()


def start_yingyongbao(**kwargs):
    hr = HandleRedis(1)
    type2 = hr.get_data_redis("yingyongbao_types")
    t = type2.split(',')[0][2:-1]
    a = 0
    for i in range(0, 2000):
        try:
            kwargs = dict(module="yingyongbao_data", data=dict(t=t, i=i))
            dicts = start(**kwargs)
            if dicts:
                log.crawler.info("获取%s的第%d页内容长度为:%d" % (type2, i, len(dicts)))
                details = dict(module="yingyongbao_save_details", data=dicts)
                # start(**details)
                comment = dict(module="yingyongbao_save_comment", data=dicts)
                # start(**comment)
                for _ in range(1):
                    threading.Thread(target=start, kwargs=details, name=None).start()
                    threading.Thread(target=start, kwargs=comment, name=None).start()
            else:
                a += 1
            if a == 10:
                break
        except Exception as e:
            raise e


def start_sougou(**kwargs):
    hr = HandleRedis(1)
    type2 = hr.get_data_redis("sougou_type").split(',')[0][2:-1]
    a = 0
    for i in range(0, 20000):
        try:
            kwargs = dict(module="sougou_content", data=dict(type1=type2, i=i))
            content = start(**kwargs)
            dicts = {"content": content}
            if content:
                log.crawler.info("获取%s的第%d页内容长度为:%d" % (type2, i, len(dicts)))
                details = dict(module="sougou_save_data", data=dicts)
                # start(**details)
                for _ in range(1):
                    threading.Thread(target=start, kwargs=details, name=None).start()
            else:
                a += 1
            if a == 10:
                break
        except Exception as e:
            log.crawler.error(e)


def start_wenshu_xingshi(**kwargs):
    r = HandleRedis(1)
    name = r.get_data_redis("wenshu_keys")
    if name:
        name = name
        print(name)
    else:
        log.crawler.info('裁判文书关键词遍历完毕.....')
        return
    index = 1
    while True:
        log.crawler.info("*" * 80)
        log.crawler.info("start crawler wenshu page is:%d" % index)
        kwargs = dict(module="wenshu_xingshi_data", data=dict(key=name, index=index), proxies=True)
        items = start(**kwargs)
        log.crawler.info("获取的文件ID长度为:%d" % (len(items) - 1))
        if len(items) == 1:
            break
        if items:
            run_eval = items[0]['RunEval']
        else:
            break
        # monkey.patch_all()
        # pool = Pool(20)
        threads = []
        for item in items[1:]:
            if threads:
                for t1 in threads:
                    if not t1.is_alive():
                        threads.remove(t1)
            if len(threads) == 10:
                time.sleep(3)
                continue
            data = {}
            data["docid"] = item["文书ID"]
            data["CASE_TYPE"] = item["案件类型"]
            data["CASE_TIME"] = item["裁判日期"]
            data["CASE_NAME"] = item["案件名称"]
            data["CASE_NUM"] = item["案号"]
            data["COURT_NAME"] = item["法院名称"]
            data['runeval'] = run_eval
            d = dict(module="wenshu_xingshi_detail", data=data, proxies=True)
            t = threading.Thread(target=start, kwargs=d, name=None)
            t.setDaemon(True)
            t.start()
            t.join()
        for t in threads:
            t.join()
        index += 1


def start_wenshu_minshi(**kwargs):
    r = HandleRedis(1)
    name = r.get_data_redis("wenshu_keys")
    if name:
        name = name
        print(name)
    else:
        log.crawler.info('裁判文书关键词遍历完毕.....')
        return
    index = 1
    while True:
        log.crawler.info("*" * 80)
        log.crawler.info("start crawler wenshu page is:%d" % index)
        kwargs = dict(module="wenshu_minshi_data", data=dict(key=name, index=index), proxies=True)
        items = start(**kwargs)
        log.crawler.info("获取的文件ID长度为:%d" % (len(items) - 1))
        if len(items) == 1:
            break
        if items:
            run_eval = items[0]['RunEval']
        else:
            break
        # monkey.patch_all()
        # pool = Pool(20)
        threads = []
        for item in items[1:]:
            if threads:
                for t1 in threads:
                    if not t1.is_alive():
                        threads.remove(t1)
            if len(threads) == 10:
                time.sleep(3)
                continue
            data = {}
            data["docid"] = item["文书ID"]
            data["CASE_TYPE"] = item["案件类型"]
            data["CASE_TIME"] = item["裁判日期"]
            data["CASE_NAME"] = item["案件名称"]
            data["CASE_NUM"] = item["案号"]
            data["COURT_NAME"] = item["法院名称"]
            data['runeval'] = run_eval
            d = dict(module="wenshu_minshi_detail", data=data, proxies=True)
            t = threading.Thread(target=start, kwargs=d, name=None)
            t.setDaemon(True)
            t.start()
            t.join()
        for t in threads:
            t.join()
        index += 1


def start_wenshu_xingzheng(**kwargs):
    r = HandleRedis(1)
    name = r.get_data_redis("wenshu_keys")
    if name:
        name = name
        print(name)
    else:
        log.crawler.info('裁判文书关键词遍历完毕.....')
        return
    index = 1
    while True:
        log.crawler.info("*" * 80)
        log.crawler.info("start crawler wenshu page is:%d" % index)
        kwargs = dict(module="wenshu_xingzheng_data", data=dict(key=name, index=index), proxies=True)
        items = start(**kwargs)
        log.crawler.info("获取的文件ID长度为:%d" % (len(items) - 1))
        if len(items) == 1:
            break
        if items:
            run_eval = items[0]['RunEval']
        else:
            break
        # monkey.patch_all()
        # pool = Pool(20)
        threads = []
        for item in items[1:]:
            if threads:
                for t1 in threads:
                    if not t1.is_alive():
                        threads.remove(t1)
            if len(threads) == 10:
                time.sleep(3)
                continue
            data = {}
            data["docid"] = item["文书ID"]
            data["CASE_TYPE"] = item["案件类型"]
            data["CASE_TIME"] = item["裁判日期"]
            data["CASE_NAME"] = item["案件名称"]
            data["CASE_NUM"] = item["案号"]
            data["COURT_NAME"] = item["法院名称"]
            data['runeval'] = run_eval
            d = dict(module="wenshu_xingzheng_detail", data=data, proxies=True)
            t = threading.Thread(target=start, kwargs=d, name=None)
            t.setDaemon(True)
            t.start()
            t.join()
        for t in threads:
            t.join()
        index += 1


def start_wenshu_peichang(**kwargs):
    r = HandleRedis(1)
    name = r.get_data_redis("wenshu_keys")
    if name:
        name = name
        print(name)
    else:
        log.crawler.info('裁判文书关键词遍历完毕.....')
        return
    index = 1
    while True:
        log.crawler.info("*" * 80)
        log.crawler.info("start crawler wenshu page is:%d" % index)
        kwargs = dict(module="wenshu_peichang_data", data=dict(key=name, index=index), proxies=True)
        items = start(**kwargs)
        log.crawler.info("获取的文件ID长度为:%d" % (len(items) - 1))
        if len(items) == 1:
            break
        if items:
            run_eval = items[0]['RunEval']
        else:
            break
        # monkey.patch_all()
        # pool = Pool(20)
        threads = []
        for item in items[1:]:
            if threads:
                for t1 in threads:
                    if not t1.is_alive():
                        threads.remove(t1)
            if len(threads) == 10:
                time.sleep(3)
                continue
            data = {}
            data["docid"] = item["文书ID"]
            data["CASE_TYPE"] = item["案件类型"]
            data["CASE_TIME"] = item["裁判日期"]
            data["CASE_NAME"] = item["案件名称"]
            data["CASE_NUM"] = item["案号"]
            data["COURT_NAME"] = item["法院名称"]
            data['runeval'] = run_eval
            d = dict(module="wenshu_peichang_detail", data=data, proxies=True)
            t = threading.Thread(target=start, kwargs=d, name=None)
            t.setDaemon(True)
            t.start()
            t.join()
        for t in threads:
            t.join()
        index += 1


def start_credit_fj():
    # r = HandleRedis(1)
    # keyword = r.get_data_redis("keywords")
    keyword = '有限'
    d = dict(module="credit_fj_list", data=dict(keyword=keyword), proxies=False)
    p1 = threading.Thread(target=start, kwargs=d, name=None)
    p1.start()
    d = dict(module="credit_fj_detail", data={}, proxies=False)
    p2 = threading.Thread(target=start, kwargs=d, name=None)
    p2.start()


if __name__ == '__main__':
    start_credit_fj()
    # start_shunqi_detail()
    # start_wenshu()
    # start_sougou()
    # start_yingyongbao()
    # start_shunqi_detail()
    # start_wenshu()
    # start_wenshu_xingshi()
    # start_wenshu_minshi()
    # start_wenshu_xingzheng()
    # start_wenshu_peichang()
