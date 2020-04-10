import logging
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, authorized_userid, setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aioredis
from conf.settings import redis_addr, pg_dsn, log_conf
from handlers.routes import setup_routes
from models.db_auth import DBAuthorizationPolicy
from aiopg.sa import create_engine
async def setup_db(app):
    pool = await aioredis.create_redis_pool(redis_addr, maxsize=20, encoding='utf-8')
    pg_pool = await create_engine(pg_dsn)

    async def close_redis(app):
        pool.close()
        pg_pool.close()
        await pool.wait_closed()
        await pg_pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    app['db_pool'] = pg_pool
    return pool, pg_pool


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


async def init_app():
    app = web.Application()
    setup_routes(app)
    redis_pool, db_pool = await setup_db(app)
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
    logging.basicConfig(**log_conf)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
