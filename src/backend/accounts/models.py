from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=False, null=False)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=True)
    # 给予每个用户1000金币, 方便后续测试
    gold = models.IntegerField(default=1000)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    email = models.EmailField(max_length=150)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)
    usage_choices = [
        ("register", "register"),
        ("reset", "reset"),
    ]
    usage = models.CharField(max_length=10, choices=usage_choices)

    def is_valid(self):
        return (timezone.now() - self.create_time).seconds < 60 * 5
