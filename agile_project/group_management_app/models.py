from django.db import models
from enum import Enum

from users_app.models import User

# groups_management_app
# grupa_projektowa, członkowstwo, (E)status_grupy

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
                              choices=[(tag.name, tag.value) for tag in ProjectGroupStatus],
                              default=ProjectGroupStatus.ACTIVE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator')
    members = models.ManyToManyField(User,
    through='GroupMember',
    through_fields=('group', 'user'),
    blank=True)

    def __str__(self):
        return f'GROUP_NAME: {self.group_name} | PROJECT_NAME: {self.project_name} | STATUS: {self.status} | members:{self.members.count()}'

class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} | {self.user.name} | {self.user.surname} |*| {self.group.group_name} | {self.group.project_name}'
