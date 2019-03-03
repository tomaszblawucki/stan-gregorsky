# Generated by Django 2.1.7 on 2019-03-03 20:08

from django.db import migrations, models
import users_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('active', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[(users_app.models.UserRoles('Regular employee'), 'Regular employee'), (users_app.models.UserRoles('Project manager'), 'Project manager')], default=users_app.models.UserRoles('Regular employee'), max_length=3)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
