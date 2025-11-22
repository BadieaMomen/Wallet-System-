from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db import transaction as db_transaction

from .models import Wallet, Transaction
from .serialize import WalletSerializer, TransactionSerialize
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from accounts.models import User
from django.db.models import Q

class WalletDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone = request.query_params.get("phone")
        if phone is None:
            return Response({"error": "wallet_id is required"}, status=400)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"error": "no user have this Phone number"}, status=404)
        try:
            wallet = Wallet.objects.get(owner=user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=404)
        rst=WalletSerializer(wallet).data
        username=rst['owner']
        userobj=User.objects.get(id=username)

        result={
            "id":rst['id'],
            "owner":userobj.username,
            "currency":rst['currency'],
            "balance":rst['balance'],
            "created_at":rst['created_at'],
        }
        return Response(result, status=200)

class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        phone = request.data.get("phone")
        amount = request.data.get("amount")
        currancy=request.data.get("currency")

        
        if currancy is None:
            return Response({"error": "phone, amount and currancy are required"}, status=400)
        if float(amount) <= 0:
            return Response({"error": "Amount must be positive"}, status=400)
        try:
            user=User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"error": "no user have this Phone number"}, status=404)
        try:
            wallet = Wallet.objects.get(owner=user,currency=currancy)
                
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"},status=status.HTTP_404_NOT_FOUND)

        with db_transaction.atomic():
            wallet.balance += amount
            wallet.save()
            trx = Transaction.objects.create(
                type="DEPOSIT",
                amount=amount,
                to_wallet=wallet,
                status="success",
                reference=f"DEP-{wallet.id}-{Transaction.objects.count()+1}"
            )
        return Response(TransactionSerialize(trx).data, status=201)

class WithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        phone = request.data.get("phone")
        amount = request.data.get("amount")
        try:
            user=User.objects.get(phone=phone)

            if user !=request.user:
                return Response({"error": "You do not own this wallet"}, status=403)
        except User.DoesNotExist:
            return Response({"error": "no user have this Phone number"}, status=404)
        try:
            wallet = Wallet.objects.get(owner=user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"},status=status.HTTP_404_NOT_FOUND)
        try:
            if amount > 0:
                pass
        except ValueError:
            return Response({"error": "Invalid amount"},status=status.HTTP_400_BAD_REQUEST)
        if wallet.balance < amount:
            return Response({"error": "Insufficient funds"},status=status.HTTP_400_BAD_REQUEST)
        with db_transaction.atomic():
            wallet.balance -= amount
            wallet.save()

            trx = Transaction.objects.create(
                type="WITHDRAW",
                amount=amount,
                from_wallet=wallet,
                status="success",
                reference=f"WDR-{wallet.id}-{Transaction.objects.count()+1}"
            )

        return Response(TransactionSerialize(trx).data, status=201)
class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sphone= request.data.get("senderphone")
        rphone = request.data.get("reciverphone")
        amount = request.data.get("amount")

        try:
            s_user = User.objects.get(phone=sphone)
            r_user = User.objects.get(phone=rphone)
        except Wallet.DoesNotExist:
            return Response({"error": "user not found"},status=status.HTTP_404_NOT_FOUND)
        try:
            if s_user == r_user:
                return Response({"error": "Cannot transfer to the same wallet"},
                                status=status.HTTP_400_BAD_REQUEST)
            if s_user is None or r_user is None:
                return Response({"error": "Invalid users"},
                                status=status.HTTP_400_BAD_REQUEST)
            if s_user != request.user:
                return Response({"error": "You do not own the sender wallet"},
                                status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"error": "Invalid users"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if s_user != request.user:
                return Response({"error": "You do not own the sender wallet"},
                                status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"error": "Invalid sender"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if amount > 0:
                pass
       
        except ValueError:
            return Response({"error": "Invalid amount"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from_wallet = Wallet.objects.get(owner=s_user)
            to_wallet = Wallet.objects.get(owner=r_user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"},status=status.HTTP_404_NOT_FOUND)  
        
        if from_wallet.balance < amount:
            return Response({"error": "Insufficient funds"},
                            status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            from_wallet.balance -= amount
            to_wallet.balance += amount
            from_wallet.save()
            to_wallet.save()

            trx = Transaction.objects.create(
                type="TRANSFER",
                amount=amount,
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                status="success",
                reference=f"TRF-{from_wallet.id}-{to_wallet.id}-{Transaction.objects.count()+1}"
            )
        return Response(TransactionSerialize(trx).data, status=201)

class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerialize

    def get_queryset(self):
        return Transaction.objects.filter(
            Q(from_wallet__owner=self.request.user) | Q(to_wallet__owner=self.request.user)
        )

# class walletquryset(APIView):
#     def get(self, request):
#         owner=request.data.get("owner")    
    
#         walletdetails=Wallet.objects.get(owner=owner)
#         return Response(
#             {
#                 "currency":walletdetails.currency,
#                 "balance":walletdetails.balance,
#                 "created_at":walletdetails.created_at,
#             }
#         )
class WalletListAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    # هذا API يعرض كل المحافظ فقط (GET)
