from rest_framework import permissions


class IsClient(permissions.BasePermission):
    """
    Give permission to rate order only if it is client's order
    """
    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
