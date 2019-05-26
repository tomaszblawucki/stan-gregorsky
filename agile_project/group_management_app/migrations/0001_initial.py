# Generated by Django 2.1.7 on 2019-05-26 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50)),
                ('project_name', models.CharField(max_length=50)),
                ('project_description', models.TextField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('planned_start_date', models.DateTimeField(auto_now_add=True)),
                ('planned_end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed')], default='Active', max_length=15)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_creator', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, through='group_management_app.GroupMember', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_management_app.ProjectGroup'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
