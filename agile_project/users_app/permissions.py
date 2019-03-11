from rest_framework.permissions import BasePermission

# custom permissions classes for models

class AuthorOnly(BasePermission):
    def has_permission(self, request, view):
        #define permission rules
        return True
