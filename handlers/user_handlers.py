from aiohttp import web


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
