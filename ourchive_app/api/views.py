from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, WorkSerializer, TagSerializer, ChapterSerializer, TagTypeSerializer, WorkTypeSerializer, BookmarkSerializer, CommentSerializer, MessageSerializer, NotificationSerializer, NotificationTypeSerializer, OurchiveSettingSerializer
from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment, Message, Notification, NotificationType, OurchiveSetting
from rest_framework import generics, permissions
from api.permissions import IsOwnerOrReadOnly, MessagePermissions, IsOwner, IsAdminOrReadOnly, IsUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'works': reverse('work-list', request=request, format=format),
        'chapters': reverse('chapter-list', request=request, format=format),
        'tagtypes': reverse('tag-type-list', request=request, format=format),
        'tags': reverse('tag-list', request=request, format=format),
        'worktypes': reverse('work-type-list', request=request, format=format),
        'bookmarks': reverse('bookmark-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
        'notifications': reverse('notification-list', request=request, format=format),
        'notificationtypes': reverse('notification-type-list', request=request, format=format),
        'settings': reverse('ourchive-setting-list', request=request, format=format),
    })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsUser]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.get_queryset().order_by('id')
    serializer_class = GroupSerializer

class WorkList(generics.ListCreateAPIView):
    queryset = Work.objects.get_queryset().order_by('id')
    serializer_class = WorkSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.get_queryset().order_by('id')
    serializer_class = WorkSerializer
    permission_classes = [IsOwnerOrReadOnly]

class WorkTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkType.objects.get_queryset().order_by('id')
    serializer_class = WorkTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class WorkTypeList(generics.ListCreateAPIView):
    queryset = WorkType.objects.get_queryset().order_by('id')
    serializer_class = WorkTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class TagTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TagType.objects.get_queryset().order_by('id')
    serializer_class = TagTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class TagTypeList(generics.ListCreateAPIView):
    queryset = TagType.objects.get_queryset().order_by('id')
    serializer_class = TagTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.get_queryset().order_by('id')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.get_queryset().order_by('id')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ChapterList(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Chapter.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.get_queryset().order_by('id')
    serializer_class = ChapterSerializer
    permission_classes = [IsOwnerOrReadOnly]

class BookmarkList(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Bookmark.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.get_queryset().order_by('id')
    serializer_class = BookmarkSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Comment.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.get_queryset().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [MessagePermissions]
    def get_queryset(self):
        return Message.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.get_queryset().order_by('id')
    serializer_class = MessageSerializer
    permission_classes = [MessagePermissions]

class NotificationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationType.objects.get_queryset().order_by('id')
    serializer_class = NotificationTypeSerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationTypeList(generics.ListCreateAPIView):
    queryset = NotificationType.objects.get_queryset().order_by('id')
    serializer_class = NotificationTypeSerializer
    permission_classes = [permissions.IsAdminUser]

class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.get_queryset().order_by('id')
    serializer_class = NotificationSerializer
    permission_classes = [IsOwner, permissions.IsAdminUser]

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.get_queryset().order_by('id')
    serializer_class = NotificationSerializer
    permission_classes = [IsOwner, permissions.IsAdminUser]

class OurchiveSettingList(generics.ListCreateAPIView):
    queryset = OurchiveSetting.objects.get_queryset().order_by('id')
    serializer_class = OurchiveSettingSerializer
    permission_classes = [IsAdminOrReadOnly]

class OurchiveSettingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurchiveSetting.objects.get_queryset().order_by('id')
    serializer_class = OurchiveSettingSerializer
    permission_classes = [IsAdminOrReadOnly]
    