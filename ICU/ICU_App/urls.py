from django.urls import path, re_path
from . import views
from . import consumers


'''
URL 라우팅 관련 설정
'''

urlpatterns = [
    path('', views.main, name='live_feed'),
]

websocket_urlpatterns = [
    re_path(r'^AIserver_ws/$', consumers.AIServerConsumer.as_asgi()),
    re_path(r'^WEBserver_ws/$', consumers.WebServerConsumer.as_asgi()),
    re_path(r'^BROWSERserver_ws/$', consumers.BrowserConsumer.as_asgi()),
]
