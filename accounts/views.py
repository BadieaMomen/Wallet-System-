from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from .models import User
from .serialize import UserSerializer

from django.views.decorators.csrf import csrf_exempt ##

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUserAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request):
        user=request.user
        user.delete()
        return Response({"message":"User deleted successfully"},status=status.HTTP_200_OK)

class LoginAPIView(APIView):

    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        user=User.objects.get(phone=phone)
        if user is None:
            return Response({"error": "Invalid phone or password"},
                            status=status.HTTP_401_UNAUTHORIZED)
        if user.password!=password:
            return Response({"error": "Invalid phone or password"},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)

class UpdateUserDetails(APIView):
    def patch(self, request):
        user=request.user
        username=request.data.get("username")
        phone=request.data.get("phone")
        password=request.data.get("password")

        if username :
            user.username=username
        if password:
            user.password=password
        if phone and phone!=user.phone:
            if User.objects.filter(phone=phone).exists():
                return Response({"error": "Phone number already in use"}, status=status.HTTP_400_BAD_REQUEST)
            user.phone=phone
        user.save()
        return Response({"message": "User details updated successfully"}, status=status.HTTP_200_OK)