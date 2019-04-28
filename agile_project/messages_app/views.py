from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated

from django.db.models import Q
from .models import Message, MessageAddressee
from users_app.models import User
from group_management_app.models import ProjectGroup, GroupMember
from .serializers import MessageSerializer, MessageSerializerForCreate, ConversationSerializer #NotificationSerializer



class ConversationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_conversation(self, request, pk=None):
        try:
            addressee = User.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response({'message':'addressee not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ConversationSerializer(data=request.data)
        response = serializer.get_conversation(addressee.pk, request.user.pk)
        serializer.mark_as_readen(addressee=request.user, sender=addressee)
        return Response(response)

    def get_recent_messages(self, request):
        serializer=ConversationSerializer(data=request.data)
        response = serializer.get_recent_messages(user=request.user)
        return Response(response)

class NotificationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_notifications(self, request):
        serializer=ConversationSerializer(data=request.data)
        response = serializer.get_notifications(user=request.user)
        return Response(response)


class ContactsList(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_contacts(self, request):
        user_groups = GroupMember.objects.filter(user=request.user)
        user_groups = [group.group for group in user_groups.all()]
        contact_groups = []
        for group in user_groups:
            partial_members = []
            for contact in group.members.filter(~Q(id=request.user.id)):
                partial_members.append(
                    {
                    'id':contact.id,
                    'email':contact.email,
                    'proffession':[proffession.proffession_name for proffession in contact.proffession.all()],
                    'name':contact.name,
                    'surname':contact.surname,
                    }
                )
            contact_groups.append({
            'group_id':group.id,
            'group_name':group.group_name,
            'project_name':group.project_name,
            'members':partial_members
            })
        return Response(contact_groups)

class ListMessages(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        serializer = MessageSerializerForCreate(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data, request.user)
        else:
            return Response({'message':f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Message was sent'})

    def list(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Message.objects.filter(addressee=request.user.id) | Message.objects.filter(sender=request.user.id)
        try:
            message = queryset.get(pk=pk)
        except:
            return Response({'message':'message not found'})
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    # def destroy(self, request, pk=None):
    #     pass

    def get_recent_messages(self, request):
        queryset = Message.objects.filter(addressee=request.user.id).order_by('-sent_date')
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_sent_messages(self, request):
        queryset = Message.objects.filter(sender=request.user.id).order_by('-sent_date')
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
