from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    reward = models.IntegerField()
    publisher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='published_tasks')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accepted_tasks', null=True, blank=True)
    
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
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
        if self.status == 'to_be_accepted':
            self.worker = worker
            self.status = 'accepted'
            self.save()
        else:
            raise Exception('Task status error')
    
    def finish(self):
        if self.status == 'accepted':
            self.status = 'finished'
            self.save()
        else:
            raise Exception('Task status error')
        
    def out_of_date(self):
        if self.status == 'to_be_accepted' and self.deadline < timezone.now():
            self.status = 'out_of_date'
            self.save()
