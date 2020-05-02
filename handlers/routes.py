from handlers.user_handlers import *
from websocket.ws import *
import aiohttp_cors


def setup_routes(app):
    app.router.add_view('/ws', WsView, name='ws')
    app.router.add_view('/', IndexView, name='index')
    app.router.add_view('/user/login', LoginView, name='login')
    app.router.add_view('/user/logout', LogoutView, name='logout')
    app.router.add_view('/users', UsersView, name='users')
    # 解决跨域请求问题
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers='*', allow_methods='*')})
    for route in list(app.router.routes()):
        cors.add(route)
