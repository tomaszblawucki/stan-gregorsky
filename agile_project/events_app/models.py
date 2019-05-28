from django.db import models
from enum import Enum

from users_app.models import User
from messages_app.models import Attachment

import pytz

utc=pytz.UTC

# events_app #
#models: Wydarzenie, pomysł, ocena_pomysłu, komentarz
# (E)typ_wydarzenia, (E)status_wydarzenia


class EventStatus(Enum):
    INIT = 'Initialized'
    RUNNING = 'In progress'
    CLOSED = 'Closed'
# TO DO

class EventType(Enum):
    BST = 'Brainstorm'
# TO DO

class RateValues(Enum):
    GOOD = 1
    BAD = -1

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True, max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=15,
                              choices = [(tag.value, tag.value) for tag in EventStatus],
                              default = EventStatus.INIT.value)
    type = models.CharField(max_length=15,
                            choices = [(tag.value, tag.value) for tag in EventType],
                            default = EventType.BST.value)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_creator')#FK
    participants = models.ManyToManyField(User,
        through='EventParticipant',
        through_fields=('event', 'user'))

    def clean(self):
        from django.core.exceptions import ValidationError
        if (self.start_date and self.end_date):
            try:
                planned_start_date = utc.localize(self.start_date)
            except:
                planned_start_date = self.start_date
            try:
                planned_end_date = utc.localize(self.end_date)
            except:
                planned_end_date = self.end_date
            if planned_start_date >= planned_end_date:
                raise ValidationError('start date cannot be greater than end date')
        if self.status not in [e.value for e in EventStatus]:
            raise ValidationError(f'invalid status value, valid values are {[tag.value for tag in EventStatus]}')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Event, self).save(*args, **kwargs)

class EventIdea(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True, max_length=1024)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_edited = models.BooleanField(default=False)


class Comment(models.Model):
    content = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edit_date = models.DateTimeField(blank=True, default=None, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(EventIdea, on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Attachment,
        through='CommentAttachment',
        through_fields=('target_comment', 'target_attachment'))

class CommentAttachment(models.Model):
    target_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    target_attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)

class EventIdeaRate(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    target_event_idea = models.ForeignKey(EventIdea, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=[(tag.value, tag.value) for tag in RateValues])

class EventParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
