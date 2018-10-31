#!/usr/bin/env python
# encoding: utf-8
'''
@author: shitian
@file: model.py
@time: 2018/10/23 10:05
@desc:

'''

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey ,INT, DATE,UniqueConstraint,Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('mysql+pymysql://spider:Za123456@@172.17.98.1:3306/anzhi?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)


class App(Base):
    __tablename__ = 'TB_APP_360'
    id = Column(Integer, primary_key=True, comment='ID')
    ahash = Column(String(100), unique=True, comment='hash(app名字+版本)')
    app_name = Column(String(100), comment='app名字')
    score = Column(String(100), comment='评分')
    comment = Column(String(100), comment='评价')
    download_num = Column(String(100), comment='下载数')
    size = Column(String(100), comment='大小')
    company = Column(String(100), comment='作者')
    update_time = Column(DateTime(), comment='更新时间')
    version = Column(String(100), comment='版本')
    sys = Column(String(100), comment='系统')
    language = Column(String(100), comment='语言')
    tag = Column(String(100), comment='标签')
    best = Column(String(100), comment='好评数')
    good = Column(String(100), comment='中评数')
    bad = Column(String(100), comment='差评数')
    crawl_time = Column(DateTime(), comment='爬取时间')


class Comment(Base):
    __tablename__ = 'TB_360APP_COMMENT'
    id = Column(Integer, primary_key=True, comment='ID')
    sid = Column(Integer, ForeignKey('TB_APP_360.id'), comment='评论id')
    app_name = Column(String(100), comment='app名字')
    user = Column(String(100), comment='用户名')
    comment = Column(Text, comment='评论')
    create_time = Column(DateTime(), comment='爬取时间')
    type = Column(String(100), comment='评论类型')
    comment_crawl_time = Column(DateTime(), comment='爬取时间')


Base.metadata.create_all(engine)