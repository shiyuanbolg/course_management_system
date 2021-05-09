# coding:utf-8
from functools import wraps
import tornado.web
import tornado.web
import tornado.escape
import hashlib
import json
import BaseHandler
import redis
from config import REDIS_HOST, REDIS_PORT

def token_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        data = json.loads(self.request.body)
        get_token = data["token"]
        print("接受到的token值为:",get_token)
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        token = r.get(get_token)
        print("现在在内存中的该token值对应的用户是:",token)
        if not token:  # 如果token在这个字典中
            data = self.wrap_json_response(code=-102, message="token has been expired")
            return self.write(data)
        return method(self, *args, **kwargs)
    return wrapper


def token_required_argment(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        get_token = self.get_argument('token', None)
        print("接受到的token值为：",get_token)
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        token = r.get(get_token)
        print("现在在内存中的该token值对应的用户是:",token)
        if not token:  # 如果token在这个字典中
            data = self.wrap_json_response(code=-102,message="token has been expired")
            return self.write(data)
        return method(self, *args, **kwargs)
    return wrapper
