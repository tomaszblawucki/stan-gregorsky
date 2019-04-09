# Generated by Django 2.1.7 on 2019-04-09 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group_management_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(max_length=1024)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('CREATED', 'created'), ('IN_PROGRESS', 'in progress'), ('COMPLETE', 'complete')], default=tasks_app.models.TaskStatus('created'), max_length=20)),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_creator', to=settings.AUTH_USER_MODEL)),
                ('project_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='group_management_app.ProjectGroup')),
            ],
        ),
    ]
