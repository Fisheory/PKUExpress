import json

from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import CustomUser
from myMessages.models import Message
from myMessages.serializers import MessageSerializer


class UserMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = f"user_{self.user.username}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


class ChatMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        sender = self.scope["user"]
        receiver_username = self.scope["url_route"]["kwargs"]["receiver"]

        if receiver_username is None:
            await self.close()
        receiver = CustomUser.objects.get(username=receiver_username)
        if receiver is None:
            await self.close()

        self.room_name = (
            f"chat_{min(sender.id, receiver.id)}_{max(sender.id, receiver.id)}"
        )

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        serializer = MessageSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message_data = serializer.data
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "message": message_data,
                    },
                )
                receiver_name = data["receiver"]
                await self.channel_layer.group_send(
                    f"user_{receiver_name}",
                    {
                        "message": message_data,
                    },
                )

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
