import random
from datetime import timedelta

from rest_framework import serializers
from django.utils import timezone

from tasks.serializers import TaskSerializer
from .models import CustomUser, VerificationCode
from .utils import send_email

class CustomUserSerializer(serializers.ModelSerializer):
    
    # 必填项
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    
    published_tasks = serializers.SerializerMethodField() # 用于返回用户发布的任务
    accepted_tasks = serializers.SerializerMethodField()  # 用于返回用户接受的任务
    accepted_accepted_tasks = serializers.SerializerMethodField() # 用于返回用户接受的任务中待完成的任务
    accepted_finished_tasks = serializers.SerializerMethodField() # 用于返回用户接受的任务中已经被完成的任务
    
    class Meta:   
        model = CustomUser
        fields = ['username', 'password', 'email', 'phone', 'gold', 'published_tasks',
                  'accepted_tasks', 'accepted_accepted_tasks', 'accepted_finished_tasks']
        
    # 检查email
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        if not value.endswith(('@pku.edu.cn', '@stu.pku.edu.cn', '@alumni.pku.edu.cn')):
            raise serializers.ValidationError('Email must be a pku email')
        return value
        
    def create(self, validated_data):
        try:
            request = self.context.get('request')
            token = request.data.get('verification_code')
        except KeyError:
            raise serializers.ValidationError('Token not found')
        
        verification_code = VerificationCode.objects.filter(
            email=validated_data['email'],
            token=token
        ).order_by('-create_time').first()
        if verification_code is None or not verification_code.is_valid():
            raise serializers.ValidationError('Invalid token')
        
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_published_tasks(self, obj):
        tasks = obj.published_tasks.all()
        # 这里用了嵌套序列化器
        return TaskSerializer(tasks, many=True).data
    
    def get_accepted_tasks(self, obj):
        tasks = obj.accepted_tasks.all()
        return TaskSerializer(tasks, many=True).data
    
    def get_accepted_accepted_tasks(self, obj):
        tasks = obj.accepted_tasks.filter(status='accepted')
        return TaskSerializer(tasks, many=True).data
    
    def get_accepted_finished_tasks(self, obj):
        tasks = obj.accepted_tasks.filter(status='finished')
        return TaskSerializer(tasks, many=True).data
        
class VerificationCodeSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    usage = serializers.ChoiceField(choices=['register', 'reset'], required=True)
    
    class Meta:
        model = VerificationCode
        fields = ['email', 'token', 'usage']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if not email.endswith(('@pku.edu.cn', '@stu.pku.edu.cn', '@alumni.pku.edu.cn')):
            raise serializers.ValidationError('Email must be a pku email')
        
        # 注册时需要email不存在, 重置密码时需要email存在
        if attrs.get('usage') == 'register' and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        elif attrs.get('usage') == 'reset' and not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist')
            
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        usage = validated_data.get('usage')
        
        # 1分钟内同一邮箱只能发送一次验证码
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if VerificationCode.objects.filter(email=email, create_time__gt=one_minute_ago).exists():
            raise serializers.ValidationError('Please wait for 1 minute before sending another token')
        
        token = f'{random.randint(100000, 999999)}'
        
        verification_code = VerificationCode.objects.create(
            email=email, token=token, usage=usage)
        
        send_email(email, token)
        
        return verification_code
