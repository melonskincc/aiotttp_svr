class RespCodeDefine:
    Success = dict(code=20000, message='ok!')
    ParamsInsufficient = dict(code=40000, message='参数错误!')
    InvalidToken = dict(code=50008, message='token错误/过期!')
    DataBaseErr = dict(code=40002, message='数据库错误!')
    UserPwdErr = dict(code=40003, message='密码或用户名错误!')
