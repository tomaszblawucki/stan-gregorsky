from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Task, TaskStatus
from users_app.models import User
from group_management_app.models import ProjectGroup
from datetime import datetime
import pytz


#description, start_Date, end_date, project_group, assigned_user
class TaskSerializer(serializers.ModelSerializer):

    def validate_for_update(self, data, task_obj):
        if not data:
            raise serializers.ValidationError('data for update was not provided')
        start_date = data.get('start_date', task_obj.start_date)
        end_date = data.get('end_date', task_obj.end_date)
        if start_date > end_date:
            raise serializers.ValidationError('start date cannot be greater than planned end date')
        return data


    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('start date cannot be greater than planned end date')
        return data

    def create(self, creator, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        assigned_user = validated_data.get('assigned_user')
        project_group = validated_data.get('project_group')
        task_obj = Task.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            creator=creator,
            )
        if assigned_user:
            assigned_user = User.objects.get(pk=assigned_user)
            task_obj.assigned_user = assigned_user
        if project_group:
            project_group = ProjectGroup.objects.get(pk=project_group)
            task_obj.project_group = project_group
        task_obj.save()

    def update(self, data, pk):
        task_obj = Task.objects.get(pk=pk)
        validated_data = self.validate_for_update(data, task_obj)
        if validated_data:
            task_obj.title = validated_data.get('title', task_obj.title)
            task_obj.description = validated_data.get('description', task_obj.description)
            task_obj.start_date = validated_data.get('start_date', task_obj.start_date)
            task_obj.end_date = validated_data.get('end_date', task_obj.end_date)
            task_status = validated_data.get('task_status', task_obj.status)
            if task_status not in TaskStatus.__members__:
                raise serializers.ValidationError('invalid task status value')
            task_obj.status = TaskStatus[task_status]
            if validated_data.get('assigned_user', False):
                try:
                    assigned_user = User.objects.get(pk=validated_data['assigned_user'])
                    task_obj.assigned_user = assigned_user
                except:
                    raise serializers.ValidationError('target user does not exist')
            if validated_data.get('project_group', False):
                try:
                    project_group = ProjectGroup.objects.get(pk=validated_data['project_group'])
                    task_obj.project_group = project_group
                except:
                    raise serializers.ValidationError({'group not exists'})
            task_obj.save()

    class Meta:
        model = Task
        fields = ('title', 'description', 'start_date', 'end_date', 'status', 'project_group', 'assigned_user', 'pk')
