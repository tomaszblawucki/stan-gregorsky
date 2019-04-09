from rest_framework.permissions import BasePermission

# custom permissions classes for models

class AuthorOnly(BasePermission):
    def has_permission(self, request, view):
        #define permission rules
        return True

class ProjectManagerOnly(BasePermission):
    def has_permission(self, request, view):
        from .models import UserRoles
        if request.user.role is UserRoles.MAN:
            return True
        return False

class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True
