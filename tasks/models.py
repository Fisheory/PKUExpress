from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_location = models.CharField(max_length=50)
    end_location = models.CharField(max_length=50)
    reward = models.IntegerField()
    start_location = models.CharField(max_length=100, blank=True, null=True)
    end_location = models.CharField(max_length=100)
    
    publisher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                                  related_name='published_tasks')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                               related_name='accepted_tasks', null=True, blank=True)
    
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    
    status_choices = [
        ('to_be_accepted', 'to_be_accepted'),
        ('accepted', 'accepted'),
        ('finished', 'finished'),
        ('out_of_date', 'out_of_date'), 
    ]
    
    status = models.CharField(max_length=20, choices=status_choices, default='to_be_accepted')
    # to_be_accepted, accepted, finished, out_of_date
    
    def __str__(self):
        return self.name
    
    def accept(self, worker):
        # 如果任务已经过期，更新self.status='out_of_date'
        self.out_of_date()
        
        if self.status == 'to_be_accepted' and self.worker is None:
            
            # Todo: 修改一下判断逻辑
            if worker.accepted_tasks.filter(status='accepted').count() >= 3: # 一个人最多接受3个任务
                raise Exception('Worker has accepted too many tasks')
            elif worker == self.publisher:
                raise Exception('Publisher cannot accept task')
          
            worker.accepted_tasks.add(self)
            worker.save()
            self.worker = worker
            self.status = 'accepted'
            self.save()
        else:
            raise Exception('Task status error')
    
    def finish(self):
        if self.status == 'accepted':
            self.status = 'finished'
            # money?
            self.worker.gold += self.reward
            self.publisher.gold -= self.reward
            
            self.finish_time = timezone.now()

            self.save()
            self.worker.save()
        else:
            raise Exception('Task status error')
        
    def out_of_date(self):
        if self.status == 'to_be_accepted' and self.deadline < timezone.now():
            self.status = 'out_of_date'
            self.save()
