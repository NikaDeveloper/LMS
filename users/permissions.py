from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Разрешает доступ к объекту, если:
    запрос безопасный (GET, HEAD, OPTIONS) - разрешаем всем,
    запрос меняющий (PUT, PATCH, DELETE) - разрешаем только владельцу объекта """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
