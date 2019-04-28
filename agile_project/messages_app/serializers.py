from rest_framework import serializers
from rest_framework.serializers import ValidationError

from django.db.models import Q

from .models import Message, MessageAddressee
from users_app.models import User
from datetime import datetime, timedelta, timezone


class ConversationSerializer(serializers.ModelSerializer):

    def get_conversation(self, addressee_pk, user_pk):
        messages = Message.objects.filter(addressee=addressee_pk, sender=user_pk, notification=False) | \
                   Message.objects.filter(addressee=user_pk, sender=addressee_pk, notification=False)
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
                'readen':message.readen,
                'datetime': message.sent_date.strftime("%Y-%m-%d %H:%M") \
                    if message.sent_date - datetime.now(timezone.utc)  < timedelta(days = -1) \
                    else message.sent_date.strftime("%H:%M:%S")
            }
            conversation.append(partial)
        return conversation

    def mark_as_readen(self, addressee, sender=None, is_notification=False):
        last_messages = Message.objects.filter(addressee=addressee, sender=sender, readen=False, notification=is_notification)
        for message in last_messages:
            message.readen = True
            message.save()
        return last_messages

    def get_recent_messages(self, user):
        recent_addressees = Message.objects.filter( (Q(addressee=user) | Q(sender=user)) & Q(notification=False) ).values('addressee', 'sender').distinct()
        recent_addressee_set = set()
        for d in recent_addressees:
            recent_addressee_set.add( d['addressee'] if d['addressee'] != user.id else d['sender'] )
        recent_messages_list = []
        recent_addressee_list = list(recent_addressee_set)
        for addressee in recent_addressee_list:
            last_message = Message.objects.filter( (Q(addressee=user, sender=addressee) | Q(addressee=addressee, sender=user)) & Q(notification=False) ).order_by('-sent_date')[0]
            recent_messages_list.append(last_message)
        response = []
        for addr, msg in zip(recent_addressee_list, recent_messages_list):
            target_user=User.objects.get(id=addr)
            partial = {
            'target_user':target_user.id,
            'target_user_email':target_user.email,
            'content':msg.content,
            'readen':msg.readen,
            'datetime':msg.sent_date,
            }
            response.append(partial)
        # recent_messages = Message.objects.get(Q(addressee=user) | Q(sender=user))
        return response

    def get_notifications(self, user):
        notifications = Message.objects.filter( (Q(addressee=user) | Q(sender=user)) & Q(notification=True) ).order_by('-sent_date')
        notification_list = []
        for notif in notifications:
            partial = {
            'creator':notif.sender.id,
            'creator_email':notif.sender.email,
            'content':notif.content,
            'datetime':notif.sent_date,
            'readen':notif.readen,
            }
            notification_list.append(partial)
        return notification_list

    class Meta:
        model=Message
        fields=('content', 'sender', 'addressee', 'sent_date')

#
# class NotificationSerializer(serializers.ModelSerializer):
#
#     def get_notifications(self, user):
#         notifications = Message.objects.filter( (Q(addressee=user) | Q(sender=user)) & Q(notification=True) ).order_by('-sent_date')
#         print(notifications)
#         notification_list = []
#         for notif in notifications:
#             partial = {
#             'creator':notif.sender.id,
#             'creator_email':notif.sender.email,
#             'content':notif.content,
#             'datetime':notif.sent_date,
#             'readen':notif.readen,
#             }
#             notification_list.append(partial)
#         return notification_list
#
#     class Meta:
#         model=Message
#         fields=('content', 'sender', 'addressee', 'sent_date', 'readen')


class MessageSerializerForCreate(serializers.ModelSerializer):

    def create(self, validated_data, user):
        sender = user
        title = validated_data.get('title')
        content = validated_data.get('content')
        addressee_pks = validated_data.get('addressee').split(',')
        is_notification = validated_data.get('notification')
        try:
            addressee = User.objects.filter(id__in=list(addressee_pks))
        except:
            raise ValidationError('Invalid addressee id')
        message_obj = Message.objects.create(
            title=title,
            content=content,
            sender=user,
            notification=is_notification or len(addressee) > 1,
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
