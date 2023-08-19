from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from ICU.ICU_App import consumers
from ICU.ICU_Config.cors_middleware import CorsMiddleware

'''
ASGI 라우팅 설정
Channels(WebSocket 비동기 통신, Django의 동기 통신 확장)
'''

# 웹 소켓 경로
websocket_urlpatterns = [
    path('AIserver_ws/', consumers.AIServerConsumer.as_asgi()),
    path('WEBserver_ws/', consumers.WebServerConsumer.as_asgi()),
    path('alerts/', consumers.AlertConsumer.as_asgi()),
]

# 웹 소켓 통신 라우팅
application = ProtocolTypeRouter({
    "websocket": CorsMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
