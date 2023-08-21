# ICU_App/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^AIserver_ws/$', consumers.AIServerConsumer.as_asgi()),
    re_path(r'^WEBserver_ws/$', consumers.WebServerConsumer.as_asgi()),
    re_path(r'^BROWSERserver_ws/$', consumers.BrowserConsumer.as_asgi()),
]
