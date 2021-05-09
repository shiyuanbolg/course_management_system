# Created by Wangcaicai at 2020/5/20

# 定义返回数据

class ReturnCode:
    SUCCESS = 0# 成功
    FAILED = -100# 失败
    DupFAILED = -101#账户不存在或者密码重复
    TIME_EXPIRE = -102 #token过期
    NO_TASK = -200 # 没有这个任务
    TASK_NO_CALCULATE = -300 # 任务未计算完成
    TASK_IS_SUCCESS = 100 # 任务计算已经完成
    TASK_NAME_EXISTS = -400 # 任务名字已经存在
    UNAUTHORIZED = 500# 未授权
    BROKEN_AUTHORIZED_DATA = -501#破损的授权数据
    WRONG_PARMAS = -101 # 参数错误
    RESOURCE_NOT_FOUND = -102 # 资源未找到
    IN_THE_CALCULATION = -103
    NULL_VALUE_IN_DATA = -104 #数据中存在空值
    WRONG_YEAR_ERROR = -105 #上传数据年份错误
    ERROR_IN_CALCULATION = -111 #计算过程出错

    @classmethod
    def message(cls,code):
        if code == cls.SUCCESS:
            return "success"
        elif code == cls.FAILED:
            return "failed"
        elif code == cls.Duplicate_name:
            return "账户已建立"
        elif code ==cls.UNAUTHORIZED:
            return "unauthorized"
        elif code == cls.BROKEN_AUTHORIZED_DATA:
            return "broken authorized data"
        elif code ==cls.WRONG_PARMAS:
            return "wrong parmas"
        elif code == cls.RESOURCE_NOT_FOUND:
            return "resource not found"
        elif code ==cls.NO_TASK:
            return "no task"
        elif code ==cls.TASK_NO_CALCULATE:
            return "task no success"
        elif code ==cls.TASK_NAME_EXISTS:
            return "task_name already exists"
        elif code ==cls.TASK_IS_SUCCESS:
            return "task is success"
        elif code ==cls.IN_THE_CALCULATION:
            return "In the calculation"
        else:
            return ''

def wrap_json_response(data =None ,code=None,message=None):
    response = {}

    if not code: #如果没传入代码,默认成功
        code = ReturnCode.SUCCESS
    if not message:
        message = ReturnCode.message(code)
    response["message"] = message
    response["result_code"] = code
    if data:
        response["data"] = data
    return response


#Minxin模式  I can


class CommonResponseMixin(object):

    @classmethod
    def wrap_json_response(cls,data=None, code=None, message=None):
        response = {}

        if not code:  # 如果没传入代码,默认成功
            code = ReturnCode.SUCCESS
        if not message:
            message = ReturnCode.message(code)
        response["message"] = message
        response["code"] = code
        if data:
            response["data"] = data
        return response
