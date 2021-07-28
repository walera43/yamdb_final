from rest_framework import permissions

from .models import UserRoles


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.role == UserRoles.ADMIN)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.role == UserRoles.ADMIN)
            or request.method in permissions.SAFE_METHODS
        )


class IsModeratorOrIsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == UserRoles.MODERATOR
        )
