from BaseHandler import BaseHandler,csrf_tokens
from tornado import gen
from config import REDIS_HOST, REDIS_PORT
import redis
from decorators import token_required,token_required_argment
import hashlib
import json
from utils.resopnse import ReturnCode, CommonResponseMixin, wrap_json_response

class UserAddCourse(BaseHandler,CommonResponseMixin):
    '''本接口为用户添加课程'''
    @gen.coroutine
    @token_required_argment
    def get(self):
            log = self.get_log_handler()
            try:
                course_id = self.get_argument("course_id", None)
                user_id = self.get_argument("user_id", None)
                if not course_id or not user_id:
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                try:
                    table_name = "user2course"
                    insert_keys = ",".join(['course_id','user_id','flag'])
                    insert_values = [course_id,user_id,1]
                    str_join = ",".join(["%s" for i in range(len(insert_values))])
                    sql = '''INSERT INTO {}({}) VALUES({})'''.format(table_name, insert_keys, str_join)
                    try:
                        yield self.insert_one(sql, insert_values)
                        data = self.wrap_json_response(code=0)
                        return self.write(data)
                    except Exception as e:
                        log.logger.error(e)
                        data = self.wrap_json_response(code=-100)
                        return self.write(data)
                except Exception as e:
                    print(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
            except Exception as e:
                data = self.wrap_json_response(code=-100)
                return self.write(data)

class UserDeleteCourse(BaseHandler,CommonResponseMixin):
    '''本接口为删除课程接口'''
    @gen.coroutine
    @token_required_argment
    def get(self):
            log = self.get_log_handler()
            try:
                course_id = self.get_argument("course_id", None)
                user_id = self.get_argument("user_id", None)
                if not course_id or not user_id:
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                try:
                    table_name = "user2course"
                    sql = '''update {} set flag=0 where course_id ={} and flag=1 and user_id={} '''.format(table_name, course_id,user_id)
                    try:
                        yield self.delete_one(sql)
                        data = self.wrap_json_response(code=0)
                        return self.write(data)
                    except Exception as e:
                        log.logger.error(e)
                        data = self.wrap_json_response(code=-100)
                        return self.write(data)
                except Exception as e:
                    print(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
            except Exception as e:
                data = self.wrap_json_response(code=-100)
                return self.write(data)

class UserShowCourse(BaseHandler,CommonResponseMixin):
    '''本接口为用户展示课程接口'''
    @gen.coroutine
    @token_required_argment
    def get(self):
            log = self.get_log_handler()
            try:
                user_id = self.get_argument("user_id", None)
                if not user_id or not user_id:
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                try:
                    table_name = "user2course"
                    sql = '''select a.course_id from {} a where a.flag=1 and a.user_id = {}'''.format(table_name,user_id)
                    res = self.find_all(sql)
                    if not res:
                        data = self.wrap_json_response(code=0)
                        return self.write(data)
                    res_data = []
                    for ans in res:
                        table_name = "course"
                        course_id = int(ans['course_id'])
                        sql = '''select a.course_name,a.coach_id,a.comments  from {} a where a.flag=1 and a.course_id = {}'''.format(table_name, course_id)
                        res1 = self.find_one(sql)
                        if not res1 :
                            data = self.wrap_json_response(code=0)
                            return self.write(data)
                        coach_id = int(res1['coach_id'])
                        sql = '''select a.user_name ,a.phone_num from coachs a where a.flag=1 and a.id = {}'''.format( coach_id)
                        res2 = self.find_one(sql)
                        if not res2 :
                            data = self.wrap_json_response(code=0)
                            return self.write(data)
                        print(res2)
                        res1.pop("coach_id")
                        res_data.append(dict(res1,**res2))
                    data = self.wrap_json_response(code=0,data=res_data)
                    return self.write(data)
                except Exception as e:
                    print(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
            except Exception as e:
                data = self.wrap_json_response(code=-100)
                return self.write(data)