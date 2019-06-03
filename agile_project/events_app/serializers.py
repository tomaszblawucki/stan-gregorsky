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
        event_name = validated_data.get('name', None)
        description = validated_data.get('description', event_obj.description)
        start_date = validated_data.get('start_date', event_obj.start_date)
        end_date = validated_data.get('end_date', event_obj.end_date)
        status = validated_data.get('status', event_obj.status)
        type = validated_data.get('type', event_obj.type)
        participants = validated_data.get('participants', None).split(',')
        present_participants = event_obj.participants.all()
        participants = set([int(p) for p  in participants]) - set([p.id for p in present_participants])
        try:
            participants = User.objects.filter(id__in=participants)
        except:
            raise ValidationError('Invalid member id')
        if event_name:
            event_obj.name = event_name
        event_obj.description = description
        event_obj.start_date = start_date
        event_obj.end_date = end_date
        event_obj.status = status
        event_obj.type = type
        try:
            event_obj.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))

        if participants:
            for participant in participants:
                event_participant = EventParticipant(
                user = participant,
                event = event_obj)
                event_participant.save()

    class Meta:
        model = Event
        fields = ('name', 'description', 'start_date', 'end_date', 'status', 'type')
        extra_kwargs = {
            'name':{'required':False},
            }


class CommentSerializerForCreate(serializers.ModelSerializer):
    def create(self, validated_data, user, idea_obj):
        content = validated_data.get('content')
        creator = user
        target = idea_obj
        comment_obj = Comment(
            content=content,
            target=target,
            creator=creator
        )
        comment_obj.save()
    class Meta:
        model = Comment
        fields=('content',)


class CommentSerializerForUpdate(serializers.ModelSerializer):
    def update(self, validated_data, comment_obj):
        content = validated_data.get('content', comment_obj.content)
        comment_obj.content = content
        comment_obj.is_edited = True
        comment_obj.edit_date = datetime.now()
        comment_obj.save()
    class Meta:
        model = Comment
        fields=('content',)


class CommentSerializerForList(serializers.ModelSerializer):
    creator_email = serializers.SerializerMethodField()
    c_date = serializers.SerializerMethodField()
    c_time = serializers.SerializerMethodField()
    e_date = serializers.SerializerMethodField()
    e_time = serializers.SerializerMethodField()

    def get_creator_email(self, obj):
        return obj.creator.email

    def get_c_date(self, obj):
        date = obj.creation_date.strftime('%Y-%m-%d')
        return date

    def get_c_time(self, obj):
        time = obj.creation_date.strftime('%H:%M')
        return time

    def get_e_date(self, obj):
        if obj.is_edited:
            date = obj.edit_date.strftime('%Y-%m-%d')
            return date
        else:
            return None

    def get_e_time(self, obj):
        if obj.is_edited:
            time = obj.edit_date.strftime('%H:%M')
            return time
        else:
            return None

    class Meta:
        model=Comment
        fields=('pk', 'content', 'creator', 'creator_email', 'creation_date', 'c_date', 'c_time', 'is_edited', 'edit_date', 'e_date', 'e_time')

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

class EventIdeaSerializerForCreate(serializers.ModelSerializer):

    def create(self, validated_data, user):
        name = validated_data.get('name')
        description = validated_data.get('description')
        event_id = validated_data.get('event')
        creator = user
        try:
            event = Event.objects.get(pk=event_id)
        except:
            raise ValidationError('Event does not exist')
        if user not in [p for p in event.participants.all()]:
            raise ValidationError('You have to be participant for this action')
        if event.status != EventStatus.RUNNING.value:
            raise ValidationError('You can add idea only in running event')
        if user not in event.participants.all():
            raise ValidationError('Only participants can add an idea to event')
        if event.status != EventStatus.RUNNING.value:
            raise ValidationError('You can add idea only for running events')
        idea_obj = EventIdea(
        name = name,
        description = description,
        event = event,
        creator = creator)
        idea_obj.save()

    class Meta:
        model = EventIdea
        fields = ('name', 'description', 'event')


class EventIdeaSerializerForUpdate(serializers.ModelSerializer):

    def update(self, validated_data, idea_obj):
        name = validated_data.get('name', idea_obj.name)
        description = validated_data.get('description', idea_obj.description)
        idea_obj.name = name
        idea_obj.description = description
        idea_obj.edited = True
        idea_obj.save()

    class Meta:
        model = EventIdea
        fields = ('name', 'description', 'event')
        extra_kwargs = {
            'event':{'required':False},
            }

class EventIdeaSerializerForList(serializers.ModelSerializer):
    positive_rates = serializers.SerializerMethodField()
    negative_rates = serializers.SerializerMethodField()
    overall_score = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()
    # creator_surname = serializers.SerializerMethodField()
    add_date = serializers.SerializerMethodField()
    add_time = serializers.SerializerMethodField()

    def get_creator_name(self, obj):
        return f'{obj.creator.name} {obj.creator.surname}'

    # def get_creator_surname(self, obj):
    #     return obj.creator.surname

    def get_positive_rates(self, obj):
        rate_cnt = EventIdeaRate.objects.filter(target_event_idea=obj, rate=1).count()
        return rate_cnt

    def get_negative_rates(self, obj):
        rate_cnt = EventIdeaRate.objects.filter(target_event_idea=obj, rate=-1).count()
        return rate_cnt

    def get_overall_score(self, obj):
        pos_rate_cnt = EventIdeaRate.objects.filter(target_event_idea=obj, rate=1).count()
        neg_rate_cnt = EventIdeaRate.objects.filter(target_event_idea=obj, rate=-1).count()
        return pos_rate_cnt - neg_rate_cnt

    def get_add_date(self, obj):
        return obj.creation_date.strftime('%Y-%m-%d')

    def get_add_time(self, obj):
        return obj.creation_date.strftime('%H:%M')

    class Meta:
        model = EventIdea
        fields = ('pk', 'name', 'creator', 'creator_name', 'description', 'positive_rates', 'negative_rates', 'overall_score', 'creation_date', 'add_date', 'add_time')


class EventSerializerForList(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    def get_participants_count(self, obj):
        return obj.participants.count()

    class Meta:
        model = Event
        fields = ('pk', 'name', 'start_date', 'end_date', 'status', 'type', 'participants_count')
