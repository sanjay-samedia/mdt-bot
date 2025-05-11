from rest_framework.permissions import BasePermission

from apps.accounts.models import UserType


class IsAdmin(BasePermission):
    message = "Only admin is allowed to perform this action."

    def has_permission(self, request, view):
        try: 
            if request.user.is_authenticated:
                return request.user.is_superuser or (request.user and request.user.user_type == UserType.ADMIN)
        except:
            return False


class IsAdminOrManager(BasePermission):
    message = "Only Manager or greater role users are allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user and request.user.user_type in [UserType.ADMIN, UserType.MANAGER]
        else:
            return False


class IsManager(BasePermission):
    message = "Only Manager or greater role users are allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user and request.user.user_type == UserType.MANAGER
        else:
            return False


class IsUser(BasePermission):
    message = "Only User is allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user and request.user.user_type == UserType.USER
        else:
            return False
