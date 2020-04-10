from aiohttp import web
from conf.define_static import ErrCodeDefine, RespCodeDefine
from models.user_models import users, make_pwd_hash
import logging
from psycopg2.errors import lookup

log = logging.getLogger(__name__)


class IndexView(web.View):
    async def get(self):
        return web.json_response({'ok': True})


class LoginView(web.View):
    async def get(self):
        return web.json_response({'ok': True})

    async def post(self):
        return web.json_response({'ok': True})


class LogoutView(web.View):
    async def get(self):
        return web.json_response({'ok': True})


class UsersView(web.View):
    async def get(self):
        log.error('a')
        async with self.request.app['db_pool'].acquire() as conn:
            s = await (await conn.execute(users.select().order_by(users.c.id))).fetchall()
        return web.json_response({'data': [dict(x) for x in s]})

    async def post(self):
        data = await self.request.json()
        username = data.get('username')
        pwd = data.get('pwd')
        email = data.get('email')
        if not all([pwd, username]):
            return web.json_response(status=ErrCodeDefine.ParamsErr)
        pwd_hash = make_pwd_hash(pwd)
        async with self.request.app['db_pool'].acquire() as conn:
            stmt = users.insert().values(username=username, email=email, password_hash=pwd_hash)
            try:
                ret = await conn.execute(stmt)
            except Exception as e:
                log.error(e)
                if hasattr(e, 'pgcode'):
                    if e.pgcode == '23505':
                        return web.json_response(RespCodeDefine.UserExist)
                    else:
                        return web.json_response(RespCodeDefine.SqlErr)
                else:
                    return web.json_response(status=ErrCodeDefine.InterServerErr)
        return web.json_response({'ok': True})

    async def delete(self):
        user_id = self.request.get('user_id')
        stmt = users.delete().where(users.c.id == user_id)
        async with self.request.app['db_pool'].acquire() as conn:
            ret = await conn.execute(stmt)
        return web.json_response({'ok': ret})
