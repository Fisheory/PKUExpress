from rest_framework import serializers
from .models import CustomUser
from tasks.serializers import TaskSerializer

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
        
    
