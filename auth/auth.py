from BaseHandler import BaseHandler,csrf_tokens
from tornado import gen
from config import REDIS_HOST, REDIS_PORT
import redis
from decorators import token_required
import hashlib
import json
from utils.resopnse import ReturnCode, CommonResponseMixin, wrap_json_response
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
'''
传参直接调用，使用前可以使用postman测试
返回结果格式统一，解析code字段，含义如下：
0：登录成功
1：数据库中没有此用户
2：用户密码输入错误
3：用户密码输入为空
前端需要记录user_id和token，后续接口每一次调用都需要传递这两个字段，用于接口鉴权
'''

'''
1、注册、登录、修改(通用)
2、会员列表、课程列表(教练)
3、教练列表（管理员) 
4、添加、修改教练--管理员
5、添加修改课程 
6、根据教练id返回教练课程
8、个人数据(教练头像)、身份
'''
class SignIn(BaseHandler,CommonResponseMixin):
    """
    本接口为三个身份的客户登录接口
    """
    @gen.coroutine
    def post(self):
        log = self.get_log_handler()
        data = json.loads(self.request.body)
        login_name = data["login_name"]
        password = data["password"]
        if not login_name or not password:
            self.write(json.dumps({"codes": "-100", "error": "empty login_user or passwrd"}))
        else:
            try:
                choice = data["choice"]
                m = hashlib.md5()
                m.update(str(password).encode("utf-8"))
                hash_passwd = m.hexdigest()
                if choice == 1:
                    tmp_x = "administer"
                elif choice == 2:
                    tmp_x = "coachs"
                elif choice == 3:
                    tmp_x = "users"
                sql = '''select a.hashed_password,a.id from {0} as a where a.user_name = "{1}" and a.flag=1'''.format(tmp_x,str(login_name))
                res = self.find_one(sql)
                if res["hashed_password"] == hash_passwd:
                    token = self.make_token(login_name)
                    data = self.wrap_json_response(code=0,data={"token":token,"id":res['id'],"profile":choice})
                    return self.write(data)
                else:
                    data = self.wrap_json_response(code=-101,message="账户不存在或者密码错误")
                    return self.write(data)
            except Exception as e:
                log.logger.error(e)
                data = self.wrap_json_response(code=-100)
                return self.write(data)


class Register(BaseHandler,CommonResponseMixin):
    '''
    三个身份用户的注册接口
    '''
    @gen.coroutine
    def post(self):
        log = self.get_log_handler()
        try:
            res_ok = self.get_res_ok()
            data = json.loads(self.request.body)
            try:
                res = {}

                user_name = data["user_name"]
                try:
                    sql = '''select user_name from users'''
                    res1 = self.find_all(sql)
                    for i in res1:
                        if i['user_name'] == user_name:
                            data = self.wrap_json_response(code=-100)
                            return self.write(data)
                    sql = '''select user_name from coachs'''
                    res1 = self.find_all(sql)
                    for i in res1:
                        if i['user_name'] == user_name:
                            data = self.wrap_json_response(code=-100)
                            return self.write(data)
                    sql = '''select user_name from administer'''
                    res1 = self.find_all(sql)
                    for i in res1:
                        if i['user_name'] == user_name:
                            data = self.wrap_json_response(code=-100)
                            return self.write(data)
                except Exception as e:
                    log.logger.error(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
                password = data["password"]
                choice = data["choice"]
                m = hashlib.md5()
                m.update(str(password).encode("utf-8"))
                hash_passwd = m.hexdigest()
                res['user_name'] = user_name
                res['hashed_password'] = hash_passwd
                res['flag'] = 1
                if choice == 1:
                    table_name = "administer"
                elif choice == 2:
                    res['phone_num'] = str(data["phone_num"])
                    table_name = "coachs"
                elif choice == 3:
                    table_name = "users"
                    res['phone_num'] = str(data["phone_num"])
                res['flag'] = 1
                insert_keys = ",".join(list(res.keys()))
                insert_values = list(res.values())
                str_join = ",".join(["%s" for i in range(len(insert_values))])
                sql = '''INSERT INTO {}({}) VALUES({})'''.format(table_name,insert_keys, str_join)
                try:
                    yield  self.insert_one(sql,insert_values)

                    log.logger.info(data)
                    data = self.wrap_json_response(code=0)
                    return self.write(data)
                except Exception as e:
                    log.logger.error(e)
                    data = self.wrap_json_response(code=-100)
                    return self.write(data)
            except Exception as e:
                log.logger.error(e)
                data = self.wrap_json_response(code=-100)
                return self.write(data)
        except Exception as e:
            log.logger.error(e)
            data = self.wrap_json_response(code=-100)
            return self.write(data)

class Delete(BaseHandler,CommonResponseMixin):
    '''
    两个身份用户删除接口
    '''
    @gen.coroutine
    def post(self):
        log = self.get_log_handler()
        try:
            data = json.loads(self.request.body)
            choice = data["choice"]
            try:
                choice = int(choice)
                user_id = data["user_id"]
                if choice == 1:
                    if not user_id:
                        data = self.wrap_json_response(code=ReturnCode.FAILED)
                        return self.write(data)
                    table_name = "users"
                    sql = '''update {} set flag=0 where id ={}'''.format(table_name, user_id)
                    self.delete_one(sql)
                    table_name = "user2course"
                    sql = '''update {} set flag=0 where user_id ={}'''.format(table_name, user_id)
                    data = self.wrap_json_response(code=0)
                    return self.write(data)
                elif choice == 2:
                    if not user_id:
                        data = self.wrap_json_response(code=ReturnCode.FAILED)
                        return self.write(data)
                    table_name = "coachs"
                    sql = '''update {} set flag=0 where id ={}'''.format(table_name, user_id)
                    self.delete_one(sql)
                    table_name = "course"
                    sql = '''update {} set flag=0 where coach_id ={} '''.format(table_name, user_id)
                    self.delete_one(sql)
                    sql = '''select a.course_id from coach2course a where flag=1 and coach_id ={}'''.format(user_id)
                    res = self.find_all(sql)
                    for i in res:
                        table_name = "lesson_time"
                        sql = '''update {} set flag=0 where course_id ={} and flag = 1'''.format(table_name,i['course_id'])
                        self.delete_one(sql)
                    table_name = "coach2course"
                    sql = '''update {} set flag=0 where coach_id ={}'''.format(table_name, user_id)
                    self.delete_one(sql)
                    data = self.wrap_json_response(code=0)
                    return self.write(data)
            except Exception as e:
                log.logger.error(e)
                data = self.wrap_json_response(code=-100)
                return self.write(data)
        except Exception as e:
            log.logger.error(e)
            data = self.wrap_json_response(code=-100)
            return self.write(data)

class SignOut(BaseHandler,CommonResponseMixin):
    @token_required
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body)
        if not data["token"]:
            data = self.wrap_json_response(code=ReturnCode.FAILED)
            return self.write(data)
        token = data["token"]
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        code = r.delete(token)


