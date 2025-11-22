from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, null=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.username