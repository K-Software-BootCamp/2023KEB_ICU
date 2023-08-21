'''
WebSocket URL 라우팅 관련 설정
'''
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^AIserver_ws/$', consumers.AIServerConsumer.as_asgi()),
    re_path(r'^WEBserver_ws/$', consumers.WebServerConsumer.as_asgi()),
    re_path(r'^VideoStreaming_ws/$', consumers.WebRTCConsumer.as_asgi()),
]
