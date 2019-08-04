from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, WorkSerializer
from api.models import Work
from rest_framework import generics

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WorkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows works to be viewed or edited.
    """
    queryset = Work.objects.all()
    serializer_class = WorkSerializer