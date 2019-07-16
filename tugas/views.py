from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAdminUser


from . import models
from . import serializers
# Create your views here

class UserListView(generics.ListCreateAPIView):
    """
    Undetailed view for Listing
    """
    permission_classes = (IsAdminUser,)
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer