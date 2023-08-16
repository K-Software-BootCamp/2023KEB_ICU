from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from ICU.ICUapp import consumers

# websocket - server path
websocket_urlpatterns = [
    re_path(r'alerts/$', consumers.AlertConsumer),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})