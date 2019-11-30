from rest_framework import permissions
from api.models import OurchiveSetting


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