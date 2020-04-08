import asyncio


async def task_a(app):
    with True:
        print('doing something...')
        await asyncio.sleep(2)
