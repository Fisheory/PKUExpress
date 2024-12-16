from django.urls import re_path
from .consumers import UserMessageConsumer, ChatMessageConsumer

websocket_urlpatterns = [
    re_path(r"ws/user/?$", UserMessageConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<receiver>\w+)/?$", ChatMessageConsumer.as_asgi()),
]
