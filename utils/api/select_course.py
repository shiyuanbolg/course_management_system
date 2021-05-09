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