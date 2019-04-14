from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Message, MessageAddressee
from users_app.models import User


class MessageSerializerForCreate(serializers.ModelSerializer):

    def create(self, validated_data, user):
        sender = user
        title = validated_data.get('title')
        content = validated_data.get('content')
        addressee_pks = validated_data.get('addressee').split(',')
        try:
            addressee = User.objects.filter(id__in=list(addressee_pks))
        except:
            raise ValidationError('Invalid addressee id')
        message_obj = Message.objects.create(
            title=title,
            content=content,
            sender=user,
            )
        message_obj.save()
        if not addressee:
            raise ValidationError('Message must have at least one existing addressee')
        for adr in addressee:
            message_addressee_obj = MessageAddressee(
                message=message_obj,
                addressee=adr
                )
            message_addressee_obj.save()

    class Meta:
        model = Message
        fields = ('title', 'content', 'addressee')

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('title', 'content', 'sent_date', 'attached_note', 'sender', 'addressee', 'attachments')



# title
# content
# sent_date
# attached_note
# addressee
# attachments
