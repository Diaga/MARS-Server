from rest_framework import permissions


def check_permission(permission, request, view):
    """Check permission explicitly"""
    if not permission().has_permission(request, view):
        view.permission_denied(
            request, message=getattr(permission, 'message', None)
        )


def check_object_permission(permission, request, view, obj):
    """Check object permission explicitly"""
    if not permission().has_object_permission(request, view, obj):
        view.permission_denied(
            request, message=getattr(permission, 'message', None)
        )


class IsAdmin(permissions.BasePermission):
    """Global permission to check if user is admin"""

    message = 'IsAdmin'

    def has_permission(self, request, view):
        """Logic to check IsAdmin"""
        return request.user.group == 'admin'


class IsNotPatient(permissions.BasePermission):
    """Global permission to check if user is not patient"""

    message = 'IsNotPatient'

    def has_permission(self, request, view):
        """Logic to check IsNotPatient"""
        return request.user.group != 'patient'
