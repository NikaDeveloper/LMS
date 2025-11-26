from rest_framework import permissions


MODERATOR_GROUP_NAME = "Moderators"


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешает доступ к объекту, если:
    запрос безопасный (GET, HEAD, OPTIONS) - разрешаем всем,
    запрос меняющий (PUT, PATCH, DELETE) - разрешаем только владельцу объекта"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsOwner(permissions.BasePermission):
    """разрешает доступ только владельцу объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    """Разрешает доступ только пользователям из группы Moderators"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
