from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(r"ws/room/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/user/(?P<userid>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
