import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ICU_Config.settings')
'''
URL routing 설정
'''
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import ICU_App.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ICU_App.routing.websocket_urlpatterns
        )
    ),
})
