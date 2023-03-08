import json

from channels.consumer import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, DenyConnection

from ..snappio.models import User


class BaseConsumer(AsyncWebsocketConsumer):
    async def set_room_group_name(self):
        """
        Set attributes for:
        self.room_name
        self.room_group_name
        """
        raise NotImplementedError("Should be implemented in subclass")

    async def connect(self):
        try:
            await self.set_room_group_name()
        except Exception:
            return await self.close(code=1000)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


@database_sync_to_async
def get_user(username: str):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception:
        return None


class UserConsumer(BaseConsumer):
    async def set_room_group_name(self):
        """
        Take the usernames from the socket route
        Sort the alphabets in alphabetical order and generate the unique room name
        since usernames are unique
        """
        if self.scope["user"].is_anonymous:
            raise DenyConnection("User is not authenticated")
        user1 = self.scope["user"].username  # first user (self)
        user2 = self.scope["url_route"]["kwargs"]["user"]  # client user
        if user1 == user2:
            raise DenyConnection("User cannot chat with self")
        userdb = await get_user(user2)
        if not userdb:
            raise DenyConnection("User does not exist")
        self.room_name = "".join(sorted(user1 + user2))
        self.room_group_name = "chat_%s" % self.room_name


class RoomConsumer(BaseConsumer):
    async def set_room_group_name(self):
        """
        Take the room name from the socket route
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
