from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]
