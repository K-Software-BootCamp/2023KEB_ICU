class CorsMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return CorsMiddlewareInstance(scope, self)


class CorsMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.middleware = middleware
        self.inner = self.middleware.inner(self.scope)

    def __call__(self, receive, send):
        async def _send(message):
            if message['type'] == 'http.response.start':
                # HTTP 요청에 대한 CORS 처리
                message['headers'] = [
                                         [b"access-control-allow-origin", b"*"],
                                         [b"access-control-allow-headers", b"*"],
                                     ] + (message.get('headers') or [])
            elif message['type'] == 'websocket.accept':
                # WebSocket 요청에 대한 CORS 처리
                message['headers'] = [
                                         [b"access-control-allow-origin", b"*"],
                                         [b"access-control-allow-headers", b"*"],
                                     ] + (message.get('headers') or [])
            await send(message)

        return self.inner(receive, _send)
