from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from users_app.models import User, UserRoles
from rest_framework.exceptions import PermissionDenied
from .serializers import EventSerializerForCreate, EventSerializerForList,\
                         EventSerializerForUpdate, EventSerializer
from users_app.models import User, UserRoles
from .models import Event, EventStatus, EventParticipant

class PermissionDecorators:
    def manager_only(fcn):
        def wrapper(*args, **kwargs):
            request = args[1]
            if not request.user.role == UserRoles.MAN.value:
                raise PermissionDenied
            return fcn( *args, **kwargs)
        return wrapper

class EventsViewSet(viewsets.ViewSet):

    @PermissionDecorators.manager_only
    def create(self, request):
        serializer = EventSerializerForCreate(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data, request.user)
        else:
            return Response({'message':f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Event created successfuly'})

    @PermissionDecorators.manager_only
    def delete(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':'Only creator can delete specified event'})
        event_obj.delete()
        return Response({'message':'Event deleted'})

    @PermissionDecorators.manager_only
    def update(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':f'Only creator can edit event data'})
        serializer = EventSerializerForUpdate(data=request.data)
        if serializer.is_valid():
            serializer.update(request.data, event_obj)
            return Response({'message':'Event updated'})
        return Response({'message':f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)


    @PermissionDecorators.manager_only
    def event_info(self, request, pk=None):
        return Response({'message':'Not done yet'}, status.HTTP_501_NOT_IMPLEMENTED)

    @PermissionDecorators.manager_only
    def close_event(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':f'Only creator can edit event data'})
        if event_obj.status == EventStatus.CLOSED.value:
            return Response({'message':'Event is already ended'})
        event_obj.status = EventStatus.CLOSED.value
        event_obj.save()
        return Response({'message':'Event status updated to `Closed`'})

    @PermissionDecorators.manager_only
    def start_event(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':f'Only creator can edit event data'})
        if event_obj.status == EventStatus.RUNNING.value:
            return Response({'message':'Event is already started'}, status.HTTP_403_FORBIDDEN)
        if event_obj.status == EventStatus.CLOSED.value:
            return Response({'message':'Event has ended'}, status.HTTP_403_FORBIDDEN)
        event_obj.status = EventStatus.RUNNING.value
        event_obj.save()
        return Response({'message':'Event status updated to `In progress`'})


    @PermissionDecorators.manager_only
    def reopen_event(self, request, pk=None):
        return Response({'message':'Not done yet'}, status.HTTP_501_NOT_IMPLEMENTED)


    def my_events(self, request):
        response = {}
        if request.user.role == UserRoles.MAN.value:
            queryset = Event.objects.filter(creator=request.user)
            serializer = EventSerializerForList(data=queryset, many=True)
            serializer.is_valid()
            response['AS CREATOR'] = serializer.data
        queryset = Event.objects.filter(participants=request.user.id).exclude(creator=request.user)
        serializer = EventSerializerForList(data=queryset, many=True)
        serializer.is_valid()
        response['AS PARTICIPANT'] = serializer.data
        return Response(response)

    def add_idea(self, request):
        pass

    def add_comment(self, request):
        pass

    def quit_event(self, request):
        pass

    def rate_idea(self, request):
        pass

    @PermissionDecorators.manager_only
    def add_participants(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':f'Only creator can add participants to event'})
        serializer = EventSerializer(data=request.data)
        try:
            serializer.add_participants(request.data, event_obj)
        except Exception as e:
            return Response({'message':str(e)}, status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Participants added'})


    @PermissionDecorators.manager_only
    def remove_participants(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if event_obj.creator != request.user:
            return Response({'message':f'Only creator can remove participants from event'})
        serializer = EventSerializer(data=request.data)
        try:
            serializer.remove_participants(request.data, event_obj)
        except Exception as e:
            return Response({'message':str(e)}, status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Participants removed'})
