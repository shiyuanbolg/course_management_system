from BaseHandler import BaseHandler,csrf_tokens
from tornado import gen
from config import REDIS_HOST, REDIS_PORT
import redis
from decorators import token_required,token_required_argment
import hashlib
import json
from utils.resopnse import ReturnCode, CommonResponseMixin, wrap_json_response

class CoachAddCourse(BaseHandler,CommonResponseMixin):
    '''本接口为教练添加课程'''
    @gen.coroutine
    @token_required
    def post(self):
            log = self.get_log_handler()
            try:
                data = json.loads(self.request.body)
                res = {}
                res["course_name"] = data["course_name"]
                res["coach_id"] = data["coach_id"]
                res["comments"] = data["comments"]
                insert_keys = ",".join(list(res.keys()))
                insert_values = list(res.values())
                str_join = ",".join(["%s" for i in range(len(insert_values))])
                table_name = "course"
                res["flag"] = 1
                sql = '''INSERT INTO {}({}) VALUES({})'''.format(table_name,insert_keys, str_join)
                try:
                    yield  self.insert_one(sql,insert_values)
                except Exception as e:
                    log.logger.error(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                sql = '''select a.course_id,a.coach_id from course a where coach_id={} and course_name="{}"'''.format(res["coach_id"],res["course_name"])
                res = self.find_one(sql)
                course_id = res["course_id"]
                coach_id = res['coach_id']
                table_name = "coach2course"
                insert_keys = "course_id,coach_id,flag"
                str_join = ",".join(["%s" for i in range(len(insert_values))])
                insert_values = [course_id,coach_id,1]
                sql = '''INSERT INTO {}({}) VALUES({})'''.format(table_name,insert_keys, str_join)
                try:
                    yield self.insert_one(sql, insert_values)
                except Exception as e:
                    log.logger.error(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                time_list = data["lesson_time"]
                for _time in time_list:
                    _time["course_id"] = course_id
                    _time["flag"] = 1
                    insert_keys = ",".join(list(_time.keys()))
                    insert_values = list(_time.values())
                    str_join = ",".join(["%s" for i in range(len(insert_values))])
                    table_name = "lesson_time"
                    sql = '''INSERT INTO {}({}) VALUES({})'''.format(table_name, insert_keys, str_join)
                    try:
                        yield self.insert_one(sql, insert_values)
                    except Exception as e:
                        log.logger.error(e)
                        data = self.wrap_json_response(code=-100)
                        return self.write(data)
                return_data = {}
                return_data['course_id'] = course_id
                sql = f'''select a.begin_day,a.end_day,a.week_day,a.day_section_begin,a.day_section_end from lesson_time a where flag=1 and a.course_id = {course_id}'''
                res = self.find_all(sql)
                res_data = []
                for ans in res:
                    tmp_res = {}
                    tmp_res['begin_day'] = ans['begin_day'].strftime('%Y-%m-%d')
                    tmp_res['end_day'] = ans['end_day'].strftime('%Y-%m-%d')
                    tmp_res['week_day'] = ans['week_day']
                    tmp_res['day_section_begin'] = str(ans['day_section_begin'])
                    tmp_res['day_section_end'] = str(ans['day_section_end'])
                    res_data.append(tmp_res)
                data = self.wrap_json_response(code=0,data=res_data)
                return self.write(data)
            except Exception as e:
               print(e)
               data = self.wrap_json_response(code=-100)
               return self.write(data)

class CoachDeleteCourse(BaseHandler,CommonResponseMixin):
    '''本接口为删除课程接口'''
    @gen.coroutine
    @token_required_argment
    def get(self):
            log = self.get_log_handler()
            try:
                course_id = self.get_argument("course_id", None)
                if not course_id:
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                try:
                    table_name = "coach2course"
                    sql = '''update {} set flag=0 where course_id ={}'''.format(table_name,course_id)
                    self.delete_one(sql)
                    table_name = "course"
                    sql = '''update {} set flag=0 where course_id ={}'''.format(table_name, course_id)
                    self.delete_one(sql)
                    table_name = "lesson_time"
                    sql = '''update {} set flag=0 where course_id ={}'''.format(table_name, course_id)
                    self.delete_one(sql)
                    data = self.wrap_json_response(code=0)
                    return self.write(data)
                except Exception as e:
                    print(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
            except Exception as e:
                data = self.wrap_json_response(code=-100)
                return self.write(data)