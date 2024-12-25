import json

from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync

from accounts.models import CustomUser
from myMessages.models import Message
from myMessages.serializers import MessageSerializer


class UserMessageConsumer(WebsocketConsumer):
    def connect(self):

        token = ""

        for key, value in self.scope["headers"]:
            if key.decode() == "authorization":
                token = value.decode().split(" ")[1]
                break

        if token is None:
            self.close()

        user_token = None

        try:
            user_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            self.close()

        if user_token is None:
            self.close()

        self.user = user_token.user

        self.room_name = f"user_{self.user.username}"

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
        print(f"disconnected: {self.channel_name}")

    def receive(self, text_data):
        pass

    def send_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))


class ChatMessageConsumer(WebsocketConsumer):
    def connect(self):

        token = ""

        for key, value in self.scope["headers"]:
            if key.decode() == "authorization":
                token = value.decode().split(" ")[1]
                break

        if token is None:
            self.close()

        user_token = None

        try:
            user_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            self.close()

        if user_token is None:
            self.close()

        self.sender = user_token.user

        receiver_username = self.scope["url_route"]["kwargs"]["receiver"]

        if receiver_username is None:
            self.close()
        receiver = CustomUser.objects.get(username=receiver_username)
        if receiver is None:
            self.close()

        self.room_name = f"chat_{min(self.sender.id, receiver.id)}_{max(self.sender.id, receiver.id)}"

        print(f"self.room_name: {self.room_name}")

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f"self.channel_name: {self.channel_name}")

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
        print(f"chat disconnected: {self.channel_name}")

    def receive(self, text_data):
        data = json.loads(text_data)
        serializer = MessageSerializer(data=data, context={"sender": self.sender})
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message_data = serializer.data
                # message_data["receiver"] = data["receiver"]
                print(message_data)
                print(f"self.room_name: {self.room_name}")
                try:
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_name,
                        {
                            "type": "chat_message",
                            "message": message_data,
                        },
                    )
                except Exception as e:
                    print(f"error sending message: {e}")
                receiver_name = data["receiver"]
                print(f"receiver_name: {receiver_name}")
                async_to_sync(self.channel_layer.group_send)(
                    f"user_{receiver_name}",
                    {
                        "type": "chat_message",
                        "message": message_data,
                    },
                )
                print("sent")

        except Exception as e:
            print(e)
            self.send(text_data=json.dumps({"error": str(e)}))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
