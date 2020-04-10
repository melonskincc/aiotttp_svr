import asyncio


async def task_a(app):
    while True:
        print('doing something...')
        await asyncio.sleep(2)
