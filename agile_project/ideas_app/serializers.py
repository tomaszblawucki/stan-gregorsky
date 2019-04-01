from rest_framework import serializers

from .models import Note, NoteAttachment, Attachment
from messages_app.models import ResourceType

class NoteSerializer(serializers.ModelSerializer):
    def create(self, creator, validated_data):
        note_obj = Note.objects.create(title=validated_data['title'],
        content=validated_data['content'],
        owner=creator)
        note_obj.save()
        if validated_data.get('attachment'):
            #may be many attachments !! TO DO
            attachment = Attachment.objects.create(uri='sample.txt', size='20000', type=ResourceType.DOC)
            note_obj.attachment.through.objects.create(note_id=note_obj.id, attachment_id=attachment.id)
        # note_obj.attachments.set(None)
        # note_obj.save()
    class Meta:
        model = Note
        fields = ('title', 'content', 'created_at', 'pk')
