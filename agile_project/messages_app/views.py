from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Message, MessageAddressee
from users_app.models import User
from .serializers import MessageSerializer, MessageSerializerForCreate, ConversationSerializer



class ConversationView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_conversation(self, request, pk=None):
        try:
            addressee = User.objects.get(id=pk)
        except Exception as e:
            print(e)
            return Response({'message':'addressee not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ConversationSerializer(data=request.data)
        serializer.get_conversation(addressee.pk, request.user.pk)
        return Response({'message':'conversation endpoint'})


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
