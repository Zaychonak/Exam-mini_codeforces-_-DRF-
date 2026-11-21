from django.shortcuts import render
from .serializer import RegisterSerializer, ProfileSerializer
from .models import User,  Profile
from rest_framework import generics, serializers, permissions


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

