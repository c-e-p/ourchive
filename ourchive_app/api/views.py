from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, WorkSerializer, TagSerializer, ChapterSerializer, TagTypeSerializer, WorkTypeSerializer, BookmarkSerializer, CommentSerializer
from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment
from rest_framework import generics, permissions
from api.permissions import IsOwnerOrReadOnly
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
    })

class UserList(generics.ListAPIView):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.get_queryset().order_by('id')
    serializer_class = GroupSerializer

class WorkList(generics.ListCreateAPIView):
    queryset = Work.objects.get_queryset().order_by('id')
    serializer_class = WorkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.get_queryset().order_by('id')
    serializer_class = WorkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

class WorkTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkType.objects.get_queryset().order_by('id')
    serializer_class = WorkTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WorkTypeList(generics.ListCreateAPIView):
    queryset = WorkType.objects.get_queryset().order_by('id')
    serializer_class = WorkTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TagType.objects.get_queryset().order_by('id')
    serializer_class = TagTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagTypeList(generics.ListCreateAPIView):
    queryset = TagType.objects.get_queryset().order_by('id')
    serializer_class = TagTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    def get_queryset(self):
        return Chapter.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.get_queryset().order_by('id')
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

class BookmarkList(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    def get_queryset(self):
        return Bookmark.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.get_queryset().order_by('id')
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    def get_queryset(self):
        return Comment.objects.get_queryset().order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.get_queryset().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

class WorkChapters(generics.ListCreateAPIView):
    queryset = Work.objects.get_queryset().order_by('id')
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        work = self.get_object()
        return Response(work.chapters.get_queryset().order_by('id'))
    