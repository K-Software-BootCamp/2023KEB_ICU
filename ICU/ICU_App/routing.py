from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/AIserver_ws/$', consumers.AIServerConsumer.as_asgi()),
    re_path(r'ws/WEBserver_ws/$', consumers.WebServerConsumer.as_asgi()),
]
