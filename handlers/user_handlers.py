from aiohttp import web
from aiohttp_cors import CorsViewMixin
from aiohttp_cors.resource_options import ResourceOptions
from conf.define_static import RespCodeDefine
from models.user_models import users, make_pwd_hash, check_pwd
import logging

log = logging.getLogger(__name__)


class IndexView(web.View, CorsViewMixin):
    # 首页视图
    cors_config = {
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
        )
    }

    async def get(self):
        return web.json_response({'ok': True})


class LoginView(web.View, CorsViewMixin):
    # 登录视图
    cors_config = {
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
        )
    }

    async def post(self):
        data = await self.request.json()
        username = data.get('username')
        pwd = data.get('password')
        if not all([username, pwd]):
            return web.json_response(RespCodeDefine.ParamsInsufficient)
        async with self.request.app['db_pool'].acquire() as conn:
            try:
                user = await (await conn.execute(users.select().where(users.c.username == username))).first()
            except Exception as e:
                log.error(e)
                return web.json_response(RespCodeDefine.DataBaseErr)
            else:
                if not user:
                    return web.json_response(RespCodeDefine.UserDoesNotExist)

                if check_pwd(pwd, user.password_hash):
                    return web.json_response(RespCodeDefine.Success)
                else:
                    return web.json_response(RespCodeDefine.PwdErr)


class LogoutView(web.View, CorsViewMixin):
    # 登出视图
    cors_config = {
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
        )
    }

    async def post(self):
        return web.json_response({'ok': True})


class UsersView(web.View, CorsViewMixin):
    # 用户视图
    cors_config = {  # 解决跨域请求问题
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
        )
    }

    async def get(self):
        # 获取用户
        async with self.request.app['db_pool'].acquire() as conn:
            s = await (await conn.execute(users.select().order_by(users.c.id))).fetchall()
        return web.json_response({'data': [dict(x) for x in s]})

    async def post(self):
        # 新增用户
        data = await self.request.json()
        username = data.get('username')
        pwd = data.get('pwd')
        email = data.get('email')
        if not all([pwd, username]):
            return web.json_response(RespCodeDefine.ParamsInsufficient)
        pwd_hash = make_pwd_hash(pwd)
        async with self.request.app['db_pool'].acquire() as conn:
            stmt = users.insert().values(username=username, email=email, password_hash=pwd_hash)
            try:
                await conn.execute(stmt)
            except Exception as e:
                log.error(e)
                if hasattr(e, 'pgcode'):
                    if e.pgcode == '23505':
                        return web.json_response(RespCodeDefine.UserExist)
                    return web.json_response(RespCodeDefine.DataBaseErr)
        return web.json_response(RespCodeDefine.Success)

    async def delete(self):
        # 删除用户
        user_id = self.request.get('user_id')
        stmt = users.delete().where(users.c.id == user_id)
        async with self.request.app['db_pool'].acquire() as conn:
            ret = await conn.execute(stmt)
        return web.json_response({'ok': ret})
