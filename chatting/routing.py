from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
import chatting.routing
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat$', consumers.ChatConsumer),
]