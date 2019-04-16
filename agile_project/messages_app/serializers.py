from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Message, MessageAddressee
from users_app.models import User
from datetime import datetime, timedelta, timezone


class ConversationSerializer(serializers.ModelSerializer):

    def get_conversation(self, addressee_pk, user_pk):
        messages = Message.objects.filter(addressee=addressee_pk, sender=user_pk) | \
                   Message.objects.filter(addressee=user_pk, sender=addressee_pk)
        conversation = []
        partial = {}
        for message in messages:
            addressee = message.addressee.first()
            sender = message.sender
            partial = {
                'owner':message.sender.id == user_pk,
                'content':message.content,
                'sender':sender.email,
                'sender_id':sender.id,
                'addressee':addressee.email,
                'addresse_id':addressee.id,
                'datetime': message.sent_date.strftime("%Y-%m-%d %H:%M") \
                    if message.sent_date - datetime.now(timezone.utc)  < timedelta(days = -1) \
                    else message.sent_date.strftime("%H:%M:%S")
            }
            conversation.append(partial)
        return conversation
        
    class Meta:
        model=Message
        fields=('content', 'sender', 'addressee', 'sent_date')

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
