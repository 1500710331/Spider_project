# coding=utf-8
import pymysql


class Mysql:
    """
    对pymysql的简单封装
    """

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def connect(self):
        """
        连接数据库
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def query(self, sql):
        """
         查询语句
         :param sql:
        :return:一个元组
        """
        cur = self.connect()
        cur.execute(sql)
        resList = cur.fetchall()

        #  查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def not_query(self, sql):
        """
        非查询语句
        :param sql:
        :return:
        """
        cur = self.connect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()