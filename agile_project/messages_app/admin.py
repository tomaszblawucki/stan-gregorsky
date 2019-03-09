from django.contrib import admin

from .models import ResourceType, Attachment, Message, MessageAddressee, MessageAttachment

# Register your models here.
admin.site.register(Attachment)
admin.site.register(Message)
admin.site.register(MessageAddressee)
admin.site.register(MessageAttachment)
