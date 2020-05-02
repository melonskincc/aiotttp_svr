import aiohttp
from aiohttp import web
from aiohttp_cors import CorsViewMixin, ResourceOptions


class WsView(web.View,CorsViewMixin):
    cors_config = {
        "*": ResourceOptions(
            allow_credentials=True,
            allow_headers="*",
        )
    }
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())

        print('websocket connection closed')

        return ws