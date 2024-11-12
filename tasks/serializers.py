from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    # source指定了展示的字段, 若不设置, 返回JSON的时候关联的用户显示的是id不方便查看
    publisher = serializers.PrimaryKeyRelatedField(read_only=True, source='publisher.username')
    worker = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='worker.username', required=False)    
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'reward',
            'start_location',
            'end_location',
            'publisher',
            'worker',
            'create_time',
            'update_time',
            'deadline',
            'status',
        ]
        read_only_fields = ['id', 'create_time', 'update_time', 'status', 'publisher']
    
    # 由于publisher设置为只读的，这里在创建任务时自动将其设为当前用户, 不允许手动修改
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['publisher'] = user
        return super().create(validated_data)
    
        