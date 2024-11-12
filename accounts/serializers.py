from rest_framework import serializers
from .models import CustomUser
from tasks.serializers import TaskSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    published_tasks = serializers.SerializerMethodField()
    accepted_tasks = serializers.SerializerMethodField()
    
    class Meta:   
        model = CustomUser
        fields = ['username', 'password', 'email', 'phone', 'gold', 'published_tasks', 'accepted_tasks']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_published_tasks(self, obj):
        tasks = obj.published_tasks.all()
        return TaskSerializer(tasks, many=True).data
    
    def get_accepted_tasks(self, obj):
        tasks = obj.accepted_tasks.all()
        return TaskSerializer(tasks, many=True).data
    