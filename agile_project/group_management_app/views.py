from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import ProjectGroup, ProjectGroupStatus, GroupMember
from . import serializers
from users_app.models import User, UserRoles
from messages_app.serializers import MessageSerializerForCreate

class ProjectGroupView(viewsets.ViewSet):
    permission_classes=(IsAuthenticated,)

    def create(self, request):
        if request.user.role != 'MAN':
            return Response({'message':'Action not permitted'}, status.HTTP_403_FORBIDDEN)
        serializer = serializers.ProjectGroupSerializerForCreate(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data, request.user)
        else:
            return Response({'message':f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Project group was created'})

    def list(self, request):
        queryset = ProjectGroup.objects.all()
        serializer = serializers.ProjectGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def list_my_groups(self, request):# groups created by PM / groups which is member
        pm_mode = request.data.get('as_manager', False)
        if pm_mode and request.user.role == 'MAN': #if user is Project Manager
            queryset = ProjectGroup.objects.filter(creator=request.user)
            serializer = serializers.ProjectGroupSerializerForList(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        else:
            queryset = ProjectGroup.objects.filter(members=request.user.id)
            serializer = serializers.ProjectGroupSerializerForList(data=queryset, many=True)
            serializer.is_valid()
            return Response(serializer.data)
        return Response({'message':'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def add_members(self, request, pk=None):
        try:
            group_obj = ProjectGroup.objects.get(pk=pk)
        except:
            return Response({'message':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != 'MAN' or request.user != group_obj.creator:
            return Response({'message':f'Action not permitted'}, status=status.HTTP_403_FORBIDDEN)

        members_ids = request.data.get('members', '').split(',')
        try:
            members=User.objects.filter(id__in=set(members_ids))
        except Exception as e:
            return Response({'message':'Invalid member id'})
        group_members = group_obj.members.all()
        message_sender = MessageSerializerForCreate(request.data)
        addressee_ids = []
        for member in members:
            if member in group_members:
                continue
            project_member_obj = GroupMember(
                user=member,
                group=group_obj
            )
            project_member_obj.save()
            addressee_ids.append(str(member.id))
        if not addressee_ids:
            return Response({'message':'All users are already members of group'}, status=status.HTTP_400_BAD_REQUEST)
        addressee_ids=','.join(addressee_ids)
        msg = {'title':'membership granted',
               'content':f'You are now member of group`{group_obj.group_name}`, granted by `{request.user.name} {request.user.surname}`. \n\
 THIS MESSAGE WAS GENERATED AUTOMATICLY, PLEASE DO NOT REPLY',
               'addressee':addressee_ids}
        message_sender.create(msg, request.user)
        return Response({'message':'members added'})


    def delete_members(self, request, pk=None):
        try:
            group_obj = ProjectGroup.objects.get(pk=pk)
        except:
            return Response({'message':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != 'MAN' or request.user != group_obj.creator:
            return Response({'message':f'Action not permitted'}, status=status.HTTP_403_FORBIDDEN)
        members_ids = request.data.get('members', '').split(',')
        members_to_delete = GroupMember.objects.filter(group=group_obj, user__in=members_ids)
        message_sender = MessageSerializerForCreate(request.data)
        addressee_ids = []
        for member in members_to_delete:
            addressee_ids.append(str(member.user.id))
            member.delete()
        # sending messages to users
        if not addressee_ids:
            return Response({'message':'None of users was members of group'}, status=status.HTTP_400_BAD_REQUEST)
        addressee_ids=','.join(addressee_ids)
        msg = {'title':'membership canceled',
               'content':f'Your membership in group `{group_obj.group_name}` was canceled by group manager `{request.user.name} {request.user.surname}`. \n\
 THIS MESSAGE WAS GENERATED AUTOMATICLY, PLEASE DO NOT REPLY',
               'addressee':addressee_ids}
        message_sender.create(msg, request.user)
        return Response({'message':'membership deleted'})

    def update(self, request, pk=None):
        try:
            group_obj = ProjectGroup.objects.get(pk=pk)
        except:
            return Response({'message':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != 'MAN' or request.user != group_obj.creator:
            return Response({'message':'Action not permitted'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ProjectGroupSerializerForUpdate(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(request.data, request.user, pk)
            return Response({'message':'Project group updated'})
        else:
            return Response(serializer.errors)

    def close_group(self, request, pk=None):
        try:
            group_obj = ProjectGroup.objects.get(pk=pk)
        except:
            return Response({'message':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != 'MAN' or request.user != group_obj.creator:
            return Response({'message':'Action not permitted'}, status=status.HTTP_403_FORBIDDEN)
        if group_obj.status == 'CLOSED':
            return Response({'message':'Group already closed'}, status.HTTP_403_FORBIDDEN)
        group_obj.status = 'CLOSED'
        group_obj.save()
        return Response({'message':'Group closed'})

    def reopen_group(self, request, pk=None):
        try:
            group_obj = ProjectGroup.objects.get(pk=pk)
        except:
            return Response({'message':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != 'MAN' or request.user != group_obj.creator:
            return Response({'message':'Action not permitted'}, status=status.HTTP_403_FORBIDDEN)
        if group_obj.status == 'ACTIVE':
            return Response({'message':'Group is already active'}, status.HTTP_403_FORBIDDEN)
        group_obj.status = 'ACTIVE'
        group_obj.save()
        return Response({'message':'Group re-opened'})

    def retrieve(self, request, pk=None):
        pass

    def get_group_members(self, request, pk=None):
        try:
            group = ProjectGroup.objects.get(id=pk, creator=request.user)
        except:
            return Response({'message':'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        members = group.members.all()
        members_list = []
        for member in members:
            partial = {
            'id':member.id,
            'email':member.email,
            'proffession':[proffession.proffession_name for proffession in member.proffession.all()],
            'name':member.name,
            'surname':member.surname,
            }
            members_list.append(partial)
        return Response(members_list)
