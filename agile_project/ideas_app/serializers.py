from rest_framework import serializers

from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    def create(self, creator, validated_data):
        print('\n',validated_data,'\n')
        note_obj = Note.objects.create(title=validated_data['title'],
        content=validated_data['content'],
        owner=creator)
        note_obj.save()
        # note_obj.attachments.set(None)
        # note_obj.save()
    class Meta:
        model = Note
        fields = ('title', 'content', 'created_at', 'attachments')
