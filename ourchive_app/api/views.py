from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, WorkSerializer
from api.models import Work
from rest_framework import generics, permissions
from api.permissions import IsOwnerOrReadOnly

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class WorkList(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]