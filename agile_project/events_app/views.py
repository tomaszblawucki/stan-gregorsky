from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from users_app.models import User, UserRoles
from rest_framework.exceptions import PermissionDenied

class PermissionDecorators:
    def manager_only(fcn):
        def wrapper(*args, **kwargs):
            request = args[1]
            if not UserRoles[request.user.role] == UserRoles.MAN:
                raise PermissionDenied
            return fcn( args[0], args[0:], **kwargs)
        return wrapper

class EventsViewSet(viewsets.ViewSet):

    @PermissionDecorators.manager_only
    def create(self, request):
        print('INSIDE CREATE')
        return Response({'message':'permission granted'})

    @PermissionDecorators.manager_only
    def delete(self, request):
        pass

    @PermissionDecorators.manager_only
    def update(self, request):
        pass

    @PermissionDecorators.manager_only
    def event_info(self, request, pk):
        pass

    @PermissionDecorators.manager_only
    def close_event(self, request, pk):
        pass

    @PermissionDecorators.manager_only
    def reopen_event(self, request, pk):
        pass

    def my_events(self, request):
        pass

    def add_idea(self, request):
        pass

    def add_comment(self, request):
        pass

    def quit_event(self, request):
        pass

    def rate_idea(self, request):
        pass

    @PermissionDecorators.manager_only
    def add_participants(self, request):
        pass

    @PermissionDecorators.manager_only
    def remove_participants(self, request):
        pass
