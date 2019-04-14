from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users_app.models import User
from .models import GroupMember, ProjectGroup, ProjectGroupStatus


class ProjectGroupSerializerForCreate(serializers.ModelSerializer):

    def create(self, validated_data, user):
        group_name = validated_data.get('group_name')
        project_name = validated_data.get('project_name')
        project_description= validated_data.get('project_description')
        planned_start_date= validated_data.get('planned_start_date')
        planned_end_date= validated_data.get('planned_end_date')
        creator=user
        members_ids = validated_data.get('members', '').split(',')
        try:
            members=User.objects.filter(id__in=set(members_ids))
        except Exception as e:
            raise ValidationError('Invalid member id')
        project_group_obj = ProjectGroup(
            group_name=group_name,
            project_name=project_name,
            project_description=project_description,
            planned_start_date=planned_start_date,
            planned_end_date=planned_end_date,
            creator=creator
        )
        project_group_obj.save()
        for member in members:
            project_member_obj = GroupMember(
                user=member,
                group=project_group_obj
            )
            project_member_obj.save()

    class Meta:
        model = ProjectGroup
        fields = ('group_name', 'project_name', 'project_description', 'planned_end_date')


class ProjectGroupSerializerForList(serializers.ModelSerializer):

    class Meta:
        model = ProjectGroup
        fields = ('pk', 'group_name', 'project_name', 'project_description', 'planned_start_date')

class ProjectGroupSerializerForUpdate(serializers.ModelSerializer):

    def validate(self, data):
        if data.planned_start_date >= data.planned_end_date:
            raise ValidationError('start date cannot be greater than end date')
        return data

    def update(self, validated_data, user, pk):
        group_obj = ProjectGroup.objects.get(pk=pk, creator=user)
        if group_obj.status == 'CLOSED':
            raise ValidationError('Cannot edit already closed project group, You have to reactivate it first')
        group_name = validated_data.get('group_name', group_obj.group_name)
        project_name = validated_data.get('project_name', group_obj.project_name)
        project_description = validated_data.get('project_description', group_obj.project_description)
        planned_start_date = validated_data.get('planned_start_date', group_obj.planned_start_date)
        planned_end_date = validated_data.get('planned_end_date', group_obj.planned_end_date)

        group_obj.group_name = group_name
        group_obj.project_name = project_name
        group_obj.project_description = project_description
        group_obj.planned_start_date = planned_start_date
        group_obj.planned_end_date = planned_end_date

        group_obj.save()

    class Meta:
        model = ProjectGroup
        fields = ('group_name', 'project_name', 'project_description', 'planned_start_date', 'planned_end_date')


class ProjectGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectGroup
        fields = ('pk', 'group_name', 'project_name', 'project_description', 'creator', 'members', 'creation_date', 'planned_start_date', 'planned_end_date')
