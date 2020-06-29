import logging, asyncio, uvloop, aioredis

import aiohttp_cors
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, authorized_userid, setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from conf.settings import redis_addr, pg_dsn, log_conf
from handlers.routes import setup_routes
from models.db_auth import DBAuthorizationPolicy
from aiopg.sa import create_engine
from libs.middleware import token_auth_middleware, user_loader


async def setup_db(app):
    """初始化redis和pgdb的数据链接"""
    pool = await aioredis.create_redis_pool(redis_addr, maxsize=20, encoding='utf-8')
    pg_pool = await create_engine(pg_dsn)

    async def close_redis(app):
        pool.close()
        pg_pool.close()
        await pool.wait_closed()
        await pg_pool.wait_closed()

    """关机的时候断开链接"""
    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    app['db_pool'] = pg_pool
    return pool, pg_pool


async def clear_ws(app):
    """关机的时候断开所有ws链接"""
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


async def init_app():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application(debug=True,
                          middlewares=[token_auth_middleware(user_loader=user_loader, exclude_routes=['/user/login'])])
    setup_routes(app)
    redis_pool, db_pool = await setup_db(app)
    app['websockets'] = dict()
    app.on_shutdown.append(clear_ws)
    setup_session(app, RedisStorage(redis_pool))
    # needs to be after session setup because of `current_user_ctx_processor` jinja2设置
    # aiohttp_jinja2.setup(
    #     app,
    #     loader=jinja2.PackageLoader(PACKAGE_NAME),
    #     context_processors=[current_user_ctx_processor],
    # )

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db_pool)
    )

    return app


def main():
    # 初始化log
    logging.basicConfig(**log_conf)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
