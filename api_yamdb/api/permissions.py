from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Права доступ для пользователей."""
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.method
                in permissions.SAFE_METHODS)


class ReadOnly(permissions.BasePermission):
    """Права доступ для пользователей только чтение."""
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class ModeratorUser(permissions.BasePermission):
    """Права доступ для модератора."""
    def has_permission(self, request, view):
        return self.request.user.role == 'moderator'
