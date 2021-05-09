#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import pytz
settings = dict(
    xsrf_cookies=False,
    cookie_secret="__ldcharge:new_tech",
    login_url="/auth/signin",
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    filetemp_path=os.path.join(os.path.dirname(__file__), "filetemp"),
    code_path=os.path.join(os.path.dirname(__file__), "codes")
    # static_path="http://192.168.1.111/static",
)

listen_port = 8001
tz = pytz.timezone('Asia/Shanghai')

# REDIS相关配置
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
