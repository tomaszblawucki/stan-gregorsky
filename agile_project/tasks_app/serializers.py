from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import Task
from users_app.models import User
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
        if assigned_user:
            assigned_user = User.objects.get(pk=assigned_user)
        # project_group = validated_data.get('project_group')
        task_obj = Task.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            creator=creator,
            assigned_user=assigned_user,
            # project_group=project_group,
            )
        task_obj.save()

    def update(self, data, pk):
        task_obj = Task.objects.get(pk=pk)
        validated_data = self.validate_for_update(data, task_obj)
        if validated_data:
            task_obj.title = validated_data.get('title', task_obj.title)
            task_obj.description = validated_data.get('description', task_obj.description)
            task_obj.start_date = validated_data.get('start_date', task_obj.start_date)
            task_obj.end_date = validated_data.get('end_date', task_obj.end_date)
            task_obj.save()

        # for key in validated_data.keys():


    class Meta:
        model = Task
        fields = ('title', 'description', 'start_date', 'end_date', 'status', 'project_group', 'assigned_user', 'pk')
