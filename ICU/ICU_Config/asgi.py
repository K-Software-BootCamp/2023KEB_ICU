import os

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ICU_App import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ICU_Config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("AIserver_ws/", consumers.AIServerConsumer.as_asgi()),
            path("WEBserver_ws/", consumers.WebServerConsumer.as_asgi()),
        ])
    ),
})
