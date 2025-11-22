from django.urls import path,include
from django.contrib import admin
from . import views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import LoginAPIView
urlpatterns = [

path ('adminn/', admin.site.urls),
path('DeleteUser/',views.DeleteUserAPIView.as_view()),
path('Createuser/',views.UserCreateAPIView.as_view()),
path("updateUserDetails/",views.UpdateUserDetails.as_view()),
path("login/", LoginAPIView.as_view()),
]


