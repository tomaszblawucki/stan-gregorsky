from django.contrib import admin

from .models import Note, NoteAttachment
# ideas admin

admin.site.register(Note)
admin.site.register(NoteAttachment)
