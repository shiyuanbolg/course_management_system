from BaseHandler import BaseHandler,csrf_tokens
from tornado import gen
from decorators import token_required_argment
from utils.resopnse import ReturnCode, CommonResponseMixin
import pymysql
from datetime import datetime
class QueryListInfo(BaseHandler,CommonResponseMixin):
    """
    本接口返回所有目标的信息
    """
    @token_required_argment
    @gen.coroutine
    def get(self):
            try:
               choice = self.get_argument("choice", None)

               if not choice:
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
               choice = int(choice)
               if choice == 1:
                    sql = '''select a.id,a.user_name,a.comments ,a.phone_num from coachs a where flag=1'''
               elif choice == 2:
                    sql = '''select a.id,a.user_name,a.comments ,a.phone_num from users a where flag=1'''
               elif choice == 3:
                    sql = '''select a.course_id,a.course_name,a.comments from course a where flag=1'''
               else:
                   data = self.wrap_json_response(code=-100)
                   return self.write(data)
               res = self.find_all(sql)
               for coach in res:
                   if choice == 1 or choice == 2:
                       if not coach['comments']:
                           coach['comments'] = "无额外信息"
                       if not coach['phone_num']:
                           coach['phone_num'] = "无额外信息"
                   elif choice == 3:
                       if not coach['comments']:
                           coach['comments'] = "无额外信息"
               data = self.wrap_json_response(code=0,data=res)
               return self.write(data)
            except Exception as e:
               data = self.wrap_json_response(code=-100)
               return self.write(data)


class QuerySingleCoachCourse(BaseHandler,CommonResponseMixin):
    @gen.coroutine
    @token_required_argment
    def get(self):
        try:
            coach_id = self.get_argument("coach_id",None)
            if not id:
                data = self.wrap_json_response(code=-100)
                return self.write(data)
            sql = '''select a.course_id,a.course_name,a.comments from course a where flag=1 and coach_id ={}'''.format(coach_id)
            res = self.find_all(sql)
            for coach in res:
                if not coach['comments']:
                    coach['comments'] = "无额外信息"
            data = self.wrap_json_response(code=0, data=res)
            return self.write(data)
        except Exception as e:
            print(e)
            data = self.wrap_json_response(code=-100)
            return self.write(data)

