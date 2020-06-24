from rest_framework import permissions
from api.models import OurchiveSetting, Chapter
from django.contrib.auth.models import AnonymousUser

class Absolutely(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:            
            return True
        return obj.user == request.user or request.user.is_superuser

class RegistrationPermitted(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        setting = OurchiveSetting.objects.filter(name='Registration Permitted').first()
        if setting.value == 'False':
            return False
        else:
            return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:            
            return True

        return request.user.is_superuser

class UserAllowsComments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        work = Chapter.objects.filter(id=request.data['chapter']).first().work
        return work.comments_permitted
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:            
            return True

        return request.user.is_superuser

class UserAllowsAnonComments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(request.user, AnonymousUser):
            work = Chapter.objects.filter(id=request.data['chapter']).first().work
            return work.anon_comments_permitted
        else:
            return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:            
            return True

        return request.user.is_superuser

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:            
            return True

        return request.user.is_superuser

class MessagePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.to_user == request.user or obj.from_user == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user