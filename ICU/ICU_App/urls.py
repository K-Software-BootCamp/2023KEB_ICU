from django.urls import path, re_path
from . import views
from . import consumers
from .ICU.Local_Environment import webcam

'''
URL 라우팅 관련 설정
'''

urlpatterns = [
    path('', webcam.capture_and_send, name='live_feed'),
    path('notify/', views.notify, name='notify'),
]

websocket_urlpatterns = [
    path('AIserver_ws/', consumers.AIServerConsumer.as_asgi()),
    path('WEBserver_ws/', consumers.WebServerConsumer.as_asgi()),
]
