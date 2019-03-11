# Generated by Django 2.1.7 on 2019-03-04 22:58

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
                ('name', models.CharField(default='derp', max_length=100)),
                ('surname', models.CharField(default='derpington', max_length=100)),
                ('birth_date', models.DateField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[(users_app.models.UserRoles('Regular employee'), 'Regular employee'), (users_app.models.UserRoles('Project manager'), 'Project manager')], default=users_app.models.UserRoles('Regular employee'), max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]