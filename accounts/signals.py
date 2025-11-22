from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from .models import User
from wallet.models import Wallet

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        initailbalanc=0.00
        # إنشاء محفظة جديدة للمستخدم الذي تم إنشاؤه
        createdat=models.DateTimeField(auto_now_add=True)

        Wallet.objects.create(
            owner=instance,
            currency="YEM",
            balance=initailbalanc,
            created_at=createdat)

