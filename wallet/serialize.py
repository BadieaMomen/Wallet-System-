from rest_framework import serializers
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    # owner = UserSerializer(read_only=True)
    class Meta:
        model = Wallet
        fields = ['id','currency','owner','balance','created_at']
class TransactionSerialize(serializers.ModelSerializer):
    from_wallet = WalletSerializer(read_only=True)
    to_wallet = WalletSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','type','amount','from_wallet','to_wallet','status','created_at']