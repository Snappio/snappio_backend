from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(r"ws/room/(?P<room_name>\w+)/$", consumers.RoomConsumer.as_asgi()),
    re_path(
        r"ws/user/(?P<user>\w+)/$",
        consumers.UserConsumer.as_asgi(),
    ),
]
