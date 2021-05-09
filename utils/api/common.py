from BaseHandler import BaseHandler,csrf_tokens
from tornado import gen
from config import REDIS_HOST, REDIS_PORT
import redis
from decorators import token_required
import hashlib
import json
from utils.resopnse import ReturnCode, CommonResponseMixin, wrap_json_response

class QueryInfo(BaseHandler,CommonResponseMixin):
    @gen.coroutine
    def post(self):
        log = self.get_log_handler()
        real_ip =self.request.remote_ip
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
