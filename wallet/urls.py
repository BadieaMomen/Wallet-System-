from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
path ('adminn/', admin.site.urls),
# path('listwallet',views.walletquryset.as_view()),
# path('mm',views.listwallets),

path('Deposit/',views.DepositAPIView.as_view()),
path('Walletetails/',views.WalletDetailAPIView.as_view()),
path('Listtransactions/',views.TransactionListAPIView.as_view()),
path('withdraw/',views.WithdrawAPIView.as_view()),
path('transfer/',views.TransferAPIView.as_view()),
]
