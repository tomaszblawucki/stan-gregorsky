# Generated by Django 2.1.7 on 2019-03-09 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import messages_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ideas_app', '0001_initial'),
        ('messages_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageAddressee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
        migrations.AddField(
            model_name='attachment',
            name='size',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attachment',
            name='type',
            field=models.CharField(choices=[('DOC', 'Dokument'), ('GRAPH', 'Obraz/grafika')], default=messages_app.models.ResourceType('Obraz/grafika'), max_length=25),
        ),
        migrations.AddField(
            model_name='attachment',
            name='uri',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='attached_note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ideas_app.Note'),
        ),
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(default='', max_length=2048),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sent_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='default title', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageattachment',
            name='attachment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messages_app.Attachment'),
        ),
        migrations.AddField(
            model_name='messageattachment',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messages_app.Message'),
        ),
        migrations.AddField(
            model_name='messageaddressee',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messages_app.Message'),
        ),
        migrations.AddField(
            model_name='message',
            name='addressee',
            field=models.ManyToManyField(through='messages_app.MessageAddressee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='attachments',
            field=models.ManyToManyField(through='messages_app.MessageAttachment', to='messages_app.Attachment'),
        ),
    ]