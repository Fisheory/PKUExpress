from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

<<<<<<< HEAD
# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=False, null=False)
=======

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=True)
    # 给予每个用户1000金币, 方便后续测试
    gold = models.IntegerField(default=1000)
<<<<<<< HEAD
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class PasswordToken(models.Model):
=======

    image = models.ImageField(upload_to="user_images", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
    email = models.EmailField(max_length=150)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)
    usage_choices = [
<<<<<<< HEAD
        ('register', 'register'),
        ('reset', 'reset'),
    ]
    usage = models.CharField(max_length=10, choices=usage_choices)
    
    def is_valid(self):
        return (timezone.now() - self.create_time).seconds < 60*5
=======
        ("register", "register"),
        ("reset", "reset"),
    ]
    usage = models.CharField(max_length=10, choices=usage_choices)

    def is_valid(self):
        return (timezone.now() - self.create_time).seconds < 60 * 5
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
