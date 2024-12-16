from rest_framework import serializers

from .models import Message
from accounts.models import CustomUser
from utils.utils import Base64ImageField


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.PrimaryKeyRelatedField(
        source="sender.username", read_only=True
    )
    receiver = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all()
    )
    image = Base64ImageField(required=False)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "timestamp",
            "content_type",
            "text",
            "image",
        ]

    def validate(self, attrs):
        
        print(attrs)

        if "request" in self.context:
            user = self.context["request"].user
            attrs["sender"] = user
        elif "sender" in self.context:
            attrs["sender"] = self.context["sender"]

        if "receiver" not in attrs:
            raise serializers.ValidationError("receiver is required")

        if attrs["content_type"] == "text" and "image" in attrs:
            raise serializers.ValidationError(
                "image is not allowed when content_type is text"
            )

        if attrs["content_type"] == "text" and "text" not in attrs:
            raise serializers.ValidationError(
                "text is required when content_type is text"
            )

        if attrs["content_type"] == "image" and "text" in attrs:
            raise serializers.ValidationError(
                "text is not allowed when content_type is image"
            )

        if attrs["content_type"] == "image" and "image" not in attrs:
            raise serializers.ValidationError(
                "mage is required when content_type is image"
            )

        return attrs

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
