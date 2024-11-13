from rest_framework import serializers
from .models import CustomUser
from tasks.serializers import TaskSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    published_tasks = serializers.SerializerMethodField() # 用于返回用户发布的任务
    accepted_tasks = serializers.SerializerMethodField()  # 用于返回用户接受的任务
    accepted_accepted_tasks = serializers.SerializerMethodField() # 用于返回用户接受的任务中已经被接取的任务
    accepted_finished_tasks = serializers.SerializerMethodField() # 用于返回用户接受的任务中已经被完成的任务
    
    # Todo: finished_tasks?
    # 如果添加, 应该可以仿造accepted_tasks, 记得在fields添加
    
    class Meta:   
        model = CustomUser
        fields = ['username', 'password', 'email', 'phone', 'gold', 'published_tasks', 'accepted_tasks', 'finished_tasks']
        
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
        
    