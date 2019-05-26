from django.db import models
from enum import Enum

from users_app.models import User

# groups_management_app
# grupa_projektowa, członkowstwo, (E)status_grupy

from datetime import datetime
import pytz

utc=pytz.UTC

class ProjectGroupStatus(Enum):
    ACTIVE = 'Active' #Project group is active
    CLOSED = 'Closed' #Project has ended

class ProjectGroup(models.Model):
    group_name = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50)
    project_description = models.TextField(max_length=1024)
    creation_date = models.DateTimeField(auto_now_add=True)
    planned_start_date = models.DateTimeField(auto_now_add=True)
    planned_end_date = models.DateTimeField(null=True, blank=True, default=None)
    status = models.CharField(max_length=15,
                              choices=[(tag.value, tag.value) for tag in ProjectGroupStatus],
                              default=ProjectGroupStatus.ACTIVE.value)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator')
    members = models.ManyToManyField(User,
    through='GroupMember',
    through_fields=('group', 'user'),
    blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (self.planned_start_date and self.planned_end_date):
            return
        try:
            planned_start_date = utc.localize(self.planned_start_date)
        except:
            planned_start_date = self.planned_start_date
        try:
            planned_end_date = utc.localize(self.planned_end_date)
        except:
            planned_end_date = self.planned_end_date
        if planned_start_date >= planned_end_date:
            raise ValidationError('planned start date cannot be greater than planned end date')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProjectGroup, self).save(*args, **kwargs)

def sanitize_data(self, data, group_obj):
    start_date = data.get('planned_start_date', group_obj.planned_start_date)
    end_date = data.get('planned_end_date', group_obj.planned_end_date)
    if not (start_date and end_date):
        return data
    try:
        start_date = utc.localize(datetime.strptime(start_date, '%Y-%m-%d %H:%M'))
    except Exception as e:
        print(e)
    try:
        end_date = utc.localize(datetime.strptime(end_date, '%Y-%m-%d %H:%M'))
    except Exception as e:
        print(e)
    if start_date >= end_date:
        raise ValidationError('start date cannot be greater than end date')
    return data


    def __str__(self):
        return f'GROUP_NAME: {self.group_name} | PROJECT_NAME: {self.project_name} | STATUS: {self.status} | members:{self.members.count()}'

class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} | {self.user.name} | {self.user.surname} |*| {self.group.group_name} | {self.group.project_name}'
