from django.contrib import admin

from .models import ProjectGroup, GroupMember
# Register your models here.

admin.site.register(ProjectGroup)
admin.site.register(GroupMember)
