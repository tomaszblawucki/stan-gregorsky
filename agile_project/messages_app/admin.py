from django.contrib import admin

from .models import ResourceType, Attachment, Message, MessageAddressee, MessageAttachment


class MessageAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'sender', 'sent_date', 'readen', 'notification')

    #
    # fieldsets = (
    #     (None,
    #     {'fields':('title', 'content', 'sender', 'addressee', 'sent_date',
    #     'readen', 'notification')}
    #     )
    # )


# Register your models here.
admin.site.register(Attachment)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageAddressee)
admin.site.register(MessageAttachment)
# admin.site.register(MessagesAdmin)
