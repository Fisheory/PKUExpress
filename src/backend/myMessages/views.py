from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Message
from accounts.models import CustomUser
from .serializers import MessageSerializer


class MessageList(APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.all()
        sender = request.user
        receiver_username = request.GET.get("receiver")
        if receiver_username is None:
            return Response(
                {"msg": "provide receiver username"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )
        receiver = CustomUser.objects.get(username=receiver_username)
        if receiver is None:
            return Response(
                {"msg": "receiver not found"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        messages = Message.objects.filter(sender=sender, receiver=receiver)
        messages |= Message.objects.filter(sender=receiver, receiver=sender)
        messages = messages.order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        serializer = MessageSerializer(data=data, context={"request": request})

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=http_status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"msg": str(e)},
                status=http_status.HTTP_400_BAD_REQUEST,
            )
