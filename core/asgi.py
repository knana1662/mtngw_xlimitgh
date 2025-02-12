"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter,ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator,AllowedHostsOriginValidator

from .routing import websocket_urlpatterns
from core import transactions_status


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
asgi_application = get_asgi_application()



application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket":AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns # list of websockets url endpoints
            )
        ),
    ),
    "channel": ChannelNameRouter(
        {
            "transactions_status":transactions_status.as_asgi(), # for showing transaction status (pending,processing,success or failed)


        }
    ),

})






