# voice_call_project/routing.py

from django.urls import re_path

from voice_call_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/call/(?P<room_name>\w+)/$', consumers.CallConsumer.as_asgi()),
]
