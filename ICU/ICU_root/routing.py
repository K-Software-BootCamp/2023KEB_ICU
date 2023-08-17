from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from ICU.ICU_root import consumers
from ICU.ICU_root.cors_middleware import CorsMiddleware

websocket_urlpatterns = [
    path('alerts/', consumers.AlertConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": CorsMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
