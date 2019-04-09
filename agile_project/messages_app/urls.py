from django.urls import path

from . import views


message_create = views.ListMessages.as_view({'post':'create'})
message_list = views.ListMessages.as_view({'get':'list'})
recent_messages = views.ListMessages.as_view({'get':'get_recent_messages'})
get_message = views.ListMessages.as_view({'get':'retrieve'})

urlpatterns = [
    path('create/', message_create, name='message_create'),
    path('list/', message_list, name='message_list'),
    path('recent-messages/', recent_messages, name='recent_messages'),
    path('list/<int:pk>/', get_message, name='get_message')
]
