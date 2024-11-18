from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=False, null=False)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=True)
    # 给予每个用户1000金币, 方便后续测试
    gold = models.IntegerField(default=1000)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username