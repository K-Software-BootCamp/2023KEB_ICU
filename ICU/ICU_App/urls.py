from django.urls import path, re_path
from . import views
from . import consumers

'''
views, consumers URL 연결
'''

urlpatterns = [
    path('', views.main, name='main'),
]

websocket_urlpatterns = [
    re_path(r'^AIserver_ws/$', consumers.AIServerConsumer.as_asgi()),
    re_path(r'^WEBserver_ws/$', consumers.WebServerConsumer.as_asgi()),
    re_path(r'^VideoStreaming_ws/$', consumers.WebRTCConsumer.as_asgi()),
]
