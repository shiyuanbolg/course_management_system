# -*- coding:utf-8 -*-
import config
import sys
import os
from auth import auth
from utils.api import search,add_course,select_course
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
handlers = [
     #登录注册
    (r"/auth/signin", auth.SignIn),
    (r"/auth/register", auth.Register),
    (r"/auth/delete", auth.Delete),

    (r"/api/search_allinfo", search.QueryListInfo),
    (r"/api/coach_add_course", add_course.CoachAddCourse),
    (r"/api/coach_delete_course", add_course.CoachDeleteCourse),
    (r"/api/single_coach_course", search.QuerySingleCoachCourse),

    #用户选课
    (r"/api/user_add_course", select_course.UserAddCourse),
    (r"/api/user_delete_course", select_course.UserDeleteCourse),
    (r"/api/user_show_course", select_course.UserShowCourse),






]


