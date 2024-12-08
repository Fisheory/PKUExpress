import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser
from django.utils import timezone


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                # 从 base64 字符串中提取图片数据
                format, base64_str = data.split(";base64,")
                image_data = base64.b64decode(base64_str)
                # 使用 UUID 生成一个唯一的文件名
                file_name = f"{uuid.uuid4()}.png"
                file = ContentFile(image_data, name=file_name)
                return file
            except Exception as e:
                raise serializers.ValidationError("Invalid base64 image data.")
        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    # source指定了展示的字段, 若不设置, 返回JSON的时候关联的用户显示的是id不方便查看
    publisher = serializers.PrimaryKeyRelatedField(
        read_only=True, source="publisher.username"
    )
    worker = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source="worker.username", required=False
    )
    image = Base64ImageField(required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "reward",
            "start_location",
            "end_location",
            "publisher",
            "worker",
            "create_time",
            "update_time",
            "finish_time",
            "deadline",
            "status",
            "image",
        ]
        read_only_fields = [
            "id",
            "create_time",
            "update_time",
            "finish_time",
            "status",
            "publisher",
        ]

    def validate(self, attrs):
        # 在这里自动设置只读的publisher为当前用户
        user = self.context["request"].user
        attrs["publisher"] = user

        # 检查reward, 正数且小于用户gold
        reward = attrs.get("reward")
        if reward <= 0:
            raise serializers.ValidationError("Reward must be a positive integer")
        elif reward > user.gold:
            raise serializers.ValidationError("Insufficient gold")

        # temp: deadline 自动设置
        # deadline = timezone.now() + timezone.timedelta(days=1)
        # attrs["deadline"] = deadline

        # 检查deadline, 必须大于当前时间
        deadline = attrs.get("deadline")
        if deadline <= timezone.now():
            raise serializers.ValidationError(
                "Deadline must be later than current time"
            )

        return attrs

    # create方法调用默认的即可
