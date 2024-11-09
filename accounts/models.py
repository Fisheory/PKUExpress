from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(User):
    # phone = models.CharField(max_length=11, blank=True)
    gold = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username