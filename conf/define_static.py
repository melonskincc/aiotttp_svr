"""错误码"""


class RespCodeDefine:
    Success = dict(code=20000, message='ok!')
    UserExist = dict(code=20001, message='用户已经存在!')
    DataBaseErr = dict(code=20002, message='数据库内部错误!')
    PwdErr = dict(code=20003, message='密码错误!')
    ParamsInsufficient = dict(code=20004, message='参数不足!')
    ParamsErr = dict(code=20005, message='参数错误!')
    UserDoesNotExist = dict(code=20006, message='用户不存在!')