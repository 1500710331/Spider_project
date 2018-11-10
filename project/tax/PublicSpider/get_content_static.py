#!/usr/bin/env python
# encoding: utf-8
'''
@author: liuyd
@file: get_content.py
@time: 2018/8/17 14:50
@desc:
'''
import Levenshtein
import random
import traceback
import os
from tax.util import log
from tax.city.common.commhtml import baseSpider
from tax.city.common.common_db import generate_db_sql
from tax.city.common.Parsehtml import ParseHtml
from tax.db.basic_db import DbHandle
from tax.db.dbconfig import table_map
from urllib.parse import urlparse
from tax.util.ipproxy import get_proxies_from_redis
from tax.model.handle_redis import HandleRedis

db=DbHandle()


class PublicSpider(baseSpider):
    def get_request_content(self,**kwargs):
        url=kwargs.get("url")
        method=kwargs.get("method","get")
        data=kwargs.get("data",None)
        proxies=kwargs.get("proxies",None)
        try:
            if method=="post":
                content=self.postHtml(url=url,data=data,proxies=proxies)
                return content
            elif method=="get":
                content=self.getHtml(url=url,data=data,proxies=proxies)
                return content
        except Exception as e:
            raise e
            #log.error.info(traceback.format_exc())

    def fetch_cookies(self,**kwargs):
        url = kwargs.get("url")
        method = kwargs.get("method", "get")
        data = kwargs.get("data", None)
        proxies = kwargs.get("proxies", None)


class HandDb(object):

    original_sql = "insert into {table_name}({columns}) values {column_values}"
    def __init__(self,table):
        self.table=table

    def generate_sql_dict(self, item):
        """
        生产单条sql插入语句
        :param table: 表名
        :param item: 数据字典形式
        :return:
        """
        print(item)
        if self.table=="tb_credit":
            item['credit_level']='A'
        dbcol = []
        values = []
        for k in item:
            dbcol.append(k)
            values.append(item.get(k, ""))
        print(values)
        sql = self.original_sql.format(table_name=self.table, columns=",".join(dbcol), column_values=tuple(values))
        print(sql)
        return sql

    def generate_sql_list(self,data,cols):
        """

        :param data: list
        :param cols: list
        :return:
        """
        if self.table == "tb_credit" and 'credit_level' not in cols:
            cols.append('credit_level')
            data.append("A")
        sql=self.original_sql.format(table_name=self.table, columns=",".join(cols), column_values=tuple(data))
        print(sql)
        return sql


    def generate_sql_by_item(self,item,data_source,test=False):
        clos=['data_source']
        values=[data_source]
        for k in item:
            if k in table_map[self.table]:
                clos.append(table_map[self.table][k])
                values.append(item[k])
            else:
                if test:
                    print(k)
        sql=self.generate_sql_list(values,clos)
        return sql

    def generate_table_item(self,item,data_source):
        """

        :param table: 表名
        :param item: 汉字映射的字典
        :return:
        """
        dbitem={'data_source':data_source}
        for k1 in item:
            fdict = {}
            for k2 in table_map[self.table]:
                sim = Levenshtein.jaro_winkler(k1,k2)
                if sim>0.8:
                    #帅选相似度大于0.9的K
                    fdict[k2]=sim
            if not fdict:
                continue
            else:
                f = zip(fdict.values(),fdict.keys())
                #降序排列选择出相似度最大的K
                f1 = sorted(f, reverse=True)
                k12=f1[0][1]
                dbitem[table_map[self.table][k12]]=item[k1]
        sql=self.generate_sql_dict(dbitem)
        return sql

def get_html(**kwargs):
    ip_pool=get_proxies_from_redis()
    num=3
    while num>0:
        try:
            proxies=random.choice(ip_pool)
            method=kwargs.get("method",'get')
            data=kwargs.get("data",None)
            url=kwargs.get("url")
            r = urlparse(url)
            host = r.netloc
            p = PublicSpider(host)
            html = p.get_request_content(method=method,url=url,data=data,proxies=proxies)
            if html:
                return html
        except Exception as err:
            num-=1
            log.crawler.info("发生连接异常尝试再次连接,第%d次重连"%(3-num))
            if num==0:
                raise err

def get_html_single_thread(**kwargs):
    num=3
    while num>0:
        try:
            proxies=kwargs.get("proxies",None)
            method=kwargs.get("method",'get')
            data=kwargs.get("data",None)
            url=kwargs.get("url")
            r = urlparse(url)
            host = r.netloc
            p = PublicSpider(host)
            html = p.get_request_content(method=method,url=url,data=data,proxies=proxies)
            if html:
                return html
        except Exception as err:
            num-=1
            log.crawler.info("发生连接异常尝试再次连接,第%d次重连"%(3-num))
            if num==0:
                raise err



if __name__=='__main__':
    pass
