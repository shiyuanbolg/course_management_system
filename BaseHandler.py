#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor
import tornado.web
import hashlib
import uuid
import redis
import logging
import copy
import pymysql
from config import REDIS_HOST, REDIS_PORT#这里设置redis主机和redis的端口
from dbutils.pooled_db import PooledDB
from tornado import gen
csrf_tokens = dict()
class ApiLog(object):
    def __init__(self, file_name='/home/work/log/api.log'):
        self.logger = logging.getLogger('api_log')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(file_name, mode='a', encoding=None, delay=False)
        formatter = logging.Formatter('%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

class BaseHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(10)  # 开辟线程池 10个连接(执行者10个)

    POOL = PooledDB(
        creator=pymysql,
        maxconnections=8,  # 最大连接数
        mincached=8,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=8,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=1,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        host='localhost',
        port=3306,
        user='root',
        database='course_management_system',
        charset='utf8'
    )

    res_error = {
        "code": -1,
        "msg": "sign error",
        "data": {}
    }

    res_ok = {
        "code": 0,
        "msg": "ok",
        "data": {}
    }

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(200)
        self.finish()

    @property
    def db(self):
        return self.application.db

    @classmethod
    def new_csrf_token(cls, user_id):
        token = str(uuid.uuid4())
        # 连接redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        r.set(str(token), user_id)
        r.expire(str(token), 60 * 60 * 24)  # 设置一天token过期
        return token

    @classmethod
    def make_token(self, user_id):
        token = str(uuid.uuid4())
        # 连接redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        r.set(str(token), user_id)
        r.expire(str(token), 60 * 60 * 24)  # 设置一天token过期
        return token

    @classmethod
    def get_log_handler(log_name='/home/work/log/api.log'):
        log_name = '/Users/shiyuan/desktop/我的项目/others/course_management_system/api.log'
        log = ApiLog(log_name)
        return log

    def get_res_ok(self):
        return copy.deepcopy(self.res_ok)

    def get_res_error(self):
        return copy.deepcopy(self.res_error)

    def create_conn(self):
        conn = self.POOL.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def close_conn(self,conn, cursor):
        conn.close()
        cursor.close()

    @gen.coroutine
    def insert_one(self,sql, args):
        conn, cur = self.create_conn()
        result = cur.execute(sql, args)
        conn.commit()
        self.close_conn(conn, cur)
        return result

    def find_one(self,sql):
        conn, cur = self.create_conn()
        cur.execute(sql)
        result = cur.fetchone()
        return dict(result)

    def find_all(self,sql):
        conn, cur = self.create_conn()
        cur.execute(sql)
        result = cur.fetchall()
        return result

    def delete_one(self,sql):
        conn, cur = self.create_conn()
        cur.execute(sql)
        conn.commit()
        self.close_conn(conn, cur)




if __name__ == '__main__':
    print(BaseHandler.make_token(1))

