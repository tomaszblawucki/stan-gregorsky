from django.db import models

from users_app.models import User
from messages_app.models import Attachment


# ideas_app # przechowalnia pomysłów użytkownika
# modele: notatka

class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    attachment = models.ManyToManyField(Attachment,
        through='NoteAttachment',
        through_fields=('note', 'attachment'),
        related_name='note_attachment',
        blank=True)

class NoteAttachment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    # class Meta:
    #     auto_created = True
