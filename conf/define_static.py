"""错误码"""

class ErrCodeDefine:
    ParamsErr = 401
    UnAuthErr = 400
    NotFoundErr = 404
    InterServerErr = 500


class RespCodeDefine:
    UserExist = dict(code=2001, msg='用户已经存在!')
    SqlErr = dict(code=2002, msg='sql语句错误!')
