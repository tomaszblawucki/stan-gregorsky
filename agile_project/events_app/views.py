from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from users_app.models import User, UserRoles
from rest_framework.exceptions import PermissionDenied
from .serializers import EventSerializerForCreate, EventSerializerForList,\
                         EventSerializerForUpdate, EventSerializer, EventIdeaSerializerForCreate,\
                         EventIdeaSerializerForUpdate, EventIdeaSerializerForList
from users_app.models import User, UserRoles
from .models import Event, EventStatus, EventParticipant, EventIdea, EventIdeaRate, RateValues

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
        if type(request.data) == dict:
            data = request.data
        else:
            data = request.data.dict()
        if event_obj.name == request.data.get('name', None):
            del data['name']
        serializer = EventSerializerForUpdate(data=data)
        if serializer.is_valid():
            serializer.update(data, event_obj)
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
        serializer = EventIdeaSerializerForCreate(data=request.data)
        if serializer.is_valid():
            try:
                serializer.create(serializer.data, request.user)
            except Exception as e:
                return Response({'message':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'Idea added'})
        else:
            return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update_idea(self, request, pk=None):
        try:
            idea_obj = EventIdea.objects.get(pk=pk)
        except:
            return Response({'message':'Idea does not exist'}, status.HTTP_404_NOT_FOUND)
        if idea_obj.event.status != EventStatus.RUNNING.value:
            return Response({'message':'Cannot edit idea in closed/initialized event'})
        if request.user != idea_obj.creator:
            return Response({'message':'Only creator can edit idea'}, status.HTTP_403_FORBIDDEN)
        serializer = EventIdeaSerializerForUpdate(data=request.data)
        if serializer.is_valid():
            try:
                serializer.update(request.data, idea_obj)
            except Exception as e:
                return Response({'message', str(e)}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':serializer.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Idea updated'})

    def list_event_ideas(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'event not found'}, status.HTTP_404_NOT_FOUND)
        queryset = EventIdea.objects.filter(event=event_obj)
        serializer = EventIdeaSerializerForList(data = queryset, many=True)
        serializer.is_valid()
        return Response({'IDEAS':serializer.data})

    def rate_idea(self, request, pk=None):
        try:
            idea_obj = EventIdea.objects.get(pk=pk)
        except:
            return Response({'message':'idea not found'}, status.HTTP_404_NOT_FOUND)
        if request.user not in [p for p in idea_obj.event.participants.all()]:
            return Response({'message':'You have to be participant of corresponding event to rate ideas'}, status.HTTP_403_FORBIDDEN)
        try:
            rate = request.data.get('rate')
        except:
            return Response({'message':'rate field required'}, status.HTTP_400_BAD_REQUEST)
        try:
            rate = int(rate)
        except:
            return Response({'message':'invalid rate value'}, status.HTTP_400_BAD_REQUEST)
        if rate not in [e.value for e in RateValues]:
            return Response({'message':'rate value can be either `1` or `-1`'}, status.HTTP_400_BAD_REQUEST)
        try:
            rate_obj = EventIdeaRate.objects.get(creator=request.user, target_event_idea=idea_obj)
            rate_obj.rate = rate
            rate_obj.save()
        except:
            rate_obj = EventIdeaRate(
                creator=request.user,
                target_event_idea=idea_obj,
                rate=rate)
            rate_obj.save()
        return Response({'message':'idea rated'})

    def add_comment(self, request):
        pass

    def edit_comment(self, request, pk=None):
        pass

    def destroy_comment(self, request, pk=None):
        pass

    def quit_event(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status.HTTP_404_NOT_FOUND)
        try:
            participant_obj = EventParticipant.objects.get(user=request.user, event=event_obj)
        except:
            return Response({'message':'participant not found'}, status.HTTP_404_NOT_FOUND)
        participant_obj.delete()
        return Response({'message':'you have left event'})

    def event_participants(self, request, pk=None):
        try:
            event_obj = Event.objects.get(pk=pk)
        except:
            return Response({'message':'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(data=request.data)
        response = serializer.get_participants(event_obj)
        return Response(response)

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
