from django.db import models
from accounts.models import User

class Wallet(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ('YEM', 'YEM'),
        ("SAR", "SAR"),

    ]

    currency = models.CharField(max_length=3,default='YEM')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True) 
    # waletnumber=models.CharField(max_length=20,unique=True,default="wal1000")
    def __str__(self):
        return f"Wallet {self.id} - {self.currency} - {self.owner.username}"
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'DEPOSIT'),
        ('WITHDRAW', 'WITHDRAW'),
        ('TRANSFER', 'TRANSFER'),
    ]
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed'),
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='DEPOSIT')
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions_from',
        null=True,
        blank=True
    )
    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions_to',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    reference = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Transaction {self.id} - Amount: {self.amount} - Status: {self.status}"