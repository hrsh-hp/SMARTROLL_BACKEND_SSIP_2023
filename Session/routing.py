from .consumers import SessionConsumer
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

session_urlpatterns = [
    re_path(r"ws/session/(?P<session_id>\w+)/$", SessionConsumer.as_asgi()),
]