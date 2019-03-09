# Generated by Django 2.1.7 on 2019-03-09 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group_management_app', '0002_groupmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectgroup',
            name='members',
            field=models.ManyToManyField(through='group_management_app.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectgroup',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
