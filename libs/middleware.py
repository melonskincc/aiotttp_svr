import json
from typing import Callable, Coroutine, Tuple
from aiohttp import web
from libs import utils
from libs.resp_code_define import RespCodeDefine


async def user_loader(token: str):
    """Checks that token is valid
    It's the callback that will get the token from "Authorization" header.
    It can check that token is exist in a database or some another place.
    Args:
        token (str): A token from "Authorization" http header.
    Returns:
        Dict or something else. If the callback returns None then
        the aiohttp.web.HTTPForbidden will be raised.
    """
    user = None
    if token == 'fake-token':
        user = {'uuid': 'fake-uuid'}
    return user


def token_auth_middleware(user_loader: Callable,
                          request_property: str = 'user',
                          auth_scheme: str = 'Bearer',
                          exclude_routes: Tuple = tuple(),
                          exclude_methods: Tuple = tuple()) -> Coroutine:
    """Checks a auth token and adds a user from user_loader in request.
    Aiohttp token auth middleware, that checks the "Authorization" http header
    for token and, if it valid, runs the "user_loader" callback. If user loader
    returns a user, then middleware adds the user to request with key that
    contain the "request_property" variable, else it will raise an HTTPForbidden
    exception.
    Args:
        user_loader (Callable): User loader callback. Must return a user or
            None if user doesn't found by token.
        request_property (str, optional): Key for save in request object.
            Defaults to 'user'.
        auth_scheme (str, optional): Prefix for value in "Authorization" header.
            Defaults to 'Bearer'.
        exclude_routes: (Tuple, optional): Tuple of pathes that will be excluded.
            Defaults to empty tuple.
        exclude_methods(Tuple, optional): Tuple of http methods that will be
            excluded. Defaults to empty tuple.
    Raises:
        TypeError: If user_loader isn't callable object.
        web.HTTPUnauthorized: If "Authorization" token is missing.
        web.HTTPForbidden: Wrong token, schema or header.
    Returns:
        Coroutine: Aiohttp middleware.
    """
    if not callable(user_loader):
        raise TypeError('Must be callable')
    headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json",
               "Access-Control-Allow-Methods": "POST, GET, OPTIONS，PUT, DELETE",
               "Access-Control-Allow-Headers": "Authentication,Origin, X-Requested-With, Content-Type, Accept"}

    # objRespHead["Access-Control-Allow-Methods"]="POST, GET, OPTIONS，PUT, DELETE"
    # objRespHead["Access-Control-Allow-Headers"] = "Authentication,Origin, X-Requested-With, Content-Type, Accept"
    # objRespHead["Content-Type"] = "application/json"

    @web.middleware
    async def middleware(request, handler):
        if (utils.is_exclude(request, exclude_routes) or
                request.method in exclude_methods):
            return await handler(request)

        try:
            scheme, token = request.headers['Authorization'].strip().split(' ')
        except KeyError:
            raise web.HTTPOk(body=json.dumps(RespCodeDefine.InvalidToken), headers=headers)
        except ValueError:
            raise web.HTTPOk(body=json.dumps(RespCodeDefine.InvalidToken), headers=headers)

        if auth_scheme.lower() != scheme.lower():
            raise web.HTTPOk(body=json.dumps(RespCodeDefine.InvalidToken), headers=headers)

        user = await user_loader(token)
        if user:
            request[request_property] = user
        else:
            raise web.HTTPOk(body=json.dumps(RespCodeDefine.InvalidToken), headers=headers)

        return await handler(request)

    return middleware
