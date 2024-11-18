from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    # source指定了展示的字段, 若不设置, 返回JSON的时候关联的用户显示的是id不方便查看
    publisher = serializers.PrimaryKeyRelatedField(read_only=True, source='publisher.email')
    worker = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),
                                                source='worker.email', required=False)    
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
            'finish_time',
            'deadline',
            'status',
        ]
        read_only_fields = ['id', 'create_time', 'update_time', 'finish_time', 'status', 'publisher']
    
    def validate(self, attrs):
        # 在这里自动设置只读的publisher为当前用户
        user = self.context['request'].user
        attrs['publisher'] = user
        
        # 检查reward, 正数且小于用户gold
        reward = attrs.get('reward')
        if reward <= 0:
            raise serializers.ValidationError('Reward must be a positive integer')
        elif reward > user.gold:
            raise serializers.ValidationError('Insufficient gold')
        
        # temp: deadline 自动设置
        deadline = timezone.now() + timezone.timedelta(days=1)
        
        # 检查deadline, 必须大于当前时间
        # deadline = attrs.get('deadline')
        if deadline <= timezone.now():
            raise serializers.ValidationError('Deadline must be later than current time')
        
        return attrs
        
    # create方法调用默认的即可
        