from django.db import models
from enum import Enum

from users_app.models import User
from django.utils.timezone import now

# messages_app #
# models: wiadomosc, zalacznik, zasob, (E)rodzaj_zasobu

class ResourceType(Enum):
    DOC = 'Dokument'
    GRAPH = 'Obraz/grafika'


class Attachment(models.Model):
    uri = models.CharField(max_length=255)
    size = models.BigIntegerField()
    type = models.CharField(max_length=25,
    choices=[(tag.name, tag.value) for tag in ResourceType],
    default = ResourceType.GRAPH.value)


class Message(models.Model):
    from ideas_app.models import Note
    #break circular dependency
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2048)
    sent_date = models.DateTimeField(default=now, editable=True)
    attached_note = models.ForeignKey(Note, models.SET_NULL, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    readen = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    addressee = models.ManyToManyField(User,
        through='MessageAddressee',
        through_fields=('message', 'addressee'))
    attachments = models.ManyToManyField(Attachment,
        through='MessageAttachment',
        through_fields=('message', 'attachment'),
        blank=True)

    def __str__(self):
        return f'{self.sent_date} | {self.sender} | {self.addressee.all()} | {self.content} | {self.readen} | NOTIFICATION:{self.notification}'

class MessageAddressee(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    addressee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'message_id:{self.message.id} | content:{self.message.content[:25]}... | readen:{self.message.readen} | addressee:{self.addressee.email}'


class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
