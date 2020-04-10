import aioredis
import asyncio
import uvloop
import uuid
import msgpack


class User:
    name = "running"
    uid = str(uuid.uuid1())
    age = 18








async def push_obj():
    data = msgpack.dumps({'a':1})
    pool = await aioredis.create_redis_pool(address='redis://127.0.0.1:6379/0', encoding='utf-8')
    with await pool:
        ret = await pool.set(User.uid, data)
        print(ret)
    print(111)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.get_event_loop().run_until_complete(push_obj())
