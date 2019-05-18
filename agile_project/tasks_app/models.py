from django.db import models
from enum import Enum

from users_app.models import User
from group_management_app.models import ProjectGroup

# Tasks app #
# zadanie, (E) status zadania

class TaskStatus(Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in progress'
    COMPLETE = 'complete'


class Task(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=1024)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20,
    choices=[(tag.name, tag.value) for tag in TaskStatus],
    default=TaskStatus.CREATED)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task_creator')
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE, null=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'title:{self.title} | desc:{self.description[:20]}... | status:{self.status} | assigned_user:{self.assigned_user.email} | project:{self.project_group.project_name}'
