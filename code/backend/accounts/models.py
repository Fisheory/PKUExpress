from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True)
    # 给予每个用户1000金币, 方便后续测试
    gold = models.IntegerField(default=1000)
    
    def __str__(self):
        return self.username