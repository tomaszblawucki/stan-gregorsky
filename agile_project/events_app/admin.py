from django.contrib import admin

from .models import Event, EventIdea, Comment, CommentAttachment, EventIdeaRate

# Register your models here.
admin.site.register(Event)
admin.site.register(EventIdea)
admin.site.register(EventIdeaRate)
admin.site.register(Comment)
admin.site.register(CommentAttachment)
