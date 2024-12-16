"""
ASGI config for PKUExpress project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

<<<<<<< HEAD
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PKUExpress.settings')

application = get_asgi_application()
=======
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

from myMessages.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PKUExpress.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
