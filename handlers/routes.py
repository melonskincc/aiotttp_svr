from handlers.user_handlers import *


def setup_routes(app):
    app.router.add_view('/', IndexView, name='index')
    app.router.add_view('/user/login', LoginView, name='login')
    app.router.add_view('/user/logout', LogoutView, name='logout')
