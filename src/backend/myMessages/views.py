from django.db.models import Q, F, Max, Case, When

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
        last_message = request.GET.get("last_message")
        
        if receiver_username is None:
            
            if last_message is not None:
                all_messages = Message.objects.filter(
                    Q(sender=sender) | Q(receiver=sender)
                ).order_by("timestamp")
                
                last_messages_queryset = (
                    all_messages.annotate(
                        other_user=Case(
                            When(sender=sender, then=F("receiver")),
                            When(receiver=sender, then=F("sender")),
                        )
                    ).values("other_user")
                )
                
                last_messages = []
                for message in last_messages_queryset:
                    last_message = Message.objects.filter(
                        Q(sender=sender, receiver=message["other_user"])
                        | Q(sender=message["other_user"], receiver=sender)
                    ).order_by("-timestamp")[:1]
                    if last_message[0] not in last_messages:
                        last_messages.append(last_message[0])
                
                serializer = MessageSerializer(last_messages, many=True)
                return Response(serializer.data)
                
            else:
                messages = Message.objects.filter(receiver=sender)
                messages |= Message.objects.filter(sender=sender)
                messages = messages.order_by("timestamp")
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            
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
