from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users_app.models import User
from .models import EventStatus, EventType, RateValues, Event, EventIdea, Comment, EventIdeaRate, EventParticipant
from users_app.models import User
from datetime import datetime
import pytz

utc=pytz.UTC


class EventSerializerForCreate(serializers.ModelSerializer):

    def create(self, validated_data, user):
        event_name = validated_data.get('name')
        description = validated_data.get('description')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        status = validated_data.get('status')
        type = validated_data.get('type')
        creator = user
        participants = validated_data.get('participants', None)
        if participants:
            try:
                participants = User.objects.filter(id__in=set(participants.split(',')))
            except Exception as e:
                raise ValidationError(f'Invalid praticipant id {e}')
        event_obj = Event(
        name = event_name,
        description = description,
        start_date = start_date,
        end_date = end_date,
        creator = creator)
        if status:
            event_obj.status = status
        if type:
            event_obj.type = type
        try:
            event_obj.save()
        except Exception as e:
            raise serializers.ValidationError(e.error_dict['__all__'][0].message)

        for participant in participants:
            event_participant = EventParticipant(
            user = participant,
            event = event_obj
            )
            event_participant.save()

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'type')

class EventSerializerForUpdate(serializers.ModelSerializer):

    def update(self, validated_data, event_obj):
        if event_obj.status != EventStatus.INIT.value:
            raise ValidationError('Event have to have status => `initialized` for update')
        event_name = validated_data.get('name', event_obj.name)
        description = validated_data.get('description', event_obj.description)
        start_date = validated_data.get('start_date', event_obj.start_date)
        end_date = validated_data.get('end_date', event_obj.end_date)
        status = validated_data.get('status', event_obj.status)
        type = validated_data.get('type', event_obj.type)
        participants = validated_data.get('participants', None).split(',')

        event_obj.name = event_name
        event_obj.description = description
        event_obj.start_date = start_date
        event_obj.end_date = end_date
        event_obj.status = status
        event_obj.type = type
        try:
            event_obj.save()
        except Exception as e:
            raise serializers.ValidationError(e.error_dict['__all__'][0].message)

        if participants:
            for participant in participants:
                event_participant = EventParticipant(
                user = participant,
                event = event_obj)
                event_participant.save()

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'status', 'type')

class EventSerializer(serializers.ModelSerializer):
    def add_participants(self, request, event_obj):
        participants_ids = request.get('participants', None)
        if participants_ids:
            try:
                participants = User.objects.filter(id__in=set(participants_ids.split(',')))
            except Exception as e:
                raise ValidationError(f'Invalid praticipant id {e}')
            present_participants = event_obj.participants.all()
            for participant in participants:
                if participant in present_participants:
                    continue
                participant_obj = EventParticipant(
                    user=participant,
                    event=event_obj
                )
                participant_obj.save()
        else:
            raise ValidationError('Participants list cannot be empty')

    def remove_participants(self, request, event_obj):
        participants_ids = request.get('participants', None)
        print(participants_ids.split(','))
        if participants_ids:
            print(EventParticipant.objects.all())
            participants_do_delete = EventParticipant.objects.filter(event=event_obj, user__in=participants_ids.split(','))
            print(participants_do_delete)
            for p in participants_do_delete:
                p.delete()
        else:
            raise ValidationError('Participants list cannot be empty')

    def get_participants(self, event_obj):
        participants = event_obj.participants.all()
        response = {}
        partial = {}
        for p in participants:
            p_proffessions = [prof.proffession_name for prof in p.proffession.all()]
            print(p_proffessions)
            partial[p.pk] = {
                    'email':p.email,
                    'name':p.name,
                    'surname':p.surname,
                    'professions':p_proffessions,
                    'role':p.role,
                }
        response['participants'] = partial
        return response
    class Meta:
        model = Event

class EventSerializerForList(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    def get_participants_count(self, obj):
        return obj.participants.count()

    class Meta:
        model = Event
        fields = ('pk', 'name', 'start_date', 'end_date', 'status', 'type', 'participants_count')
