from django.urls import path

from . import views


message_create = views.ListMessages.as_view({'post':'create'})
message_list = views.ListMessages.as_view({'get':'list'})
recent_messages = views.ListMessages.as_view({'get':'get_recent_messages'})
sent_messages = views.ListMessages.as_view({'get':'get_sent_messages'})
get_message = views.ListMessages.as_view({'get':'retrieve'})
conversation = views.ConversationView.as_view({'get':'get_conversation'})

# get_notifications = views.ListNotifications.as_view({'get':'get_notifications'})
get_recent_messages = views.ConversationView.as_view({'get':'get_recent_messages'})
get_notifications = views.NotificationView.as_view({'get':'get_notifications'})

get_contacts = views.ContactsList.as_view({'get':'get_contacts'})


urlpatterns = [
    path('create/', message_create, name='message_create'),
    # path('list/', message_list, name='message_list'),
    # path('recent-messages/', recent_messages, name='recent_messages'),
    path('sent-messages/', recent_messages, name='sent_messages'),
    path('<int:pk>/', get_message, name='get_message'),

    path('conversation/<int:pk>/', conversation, name='conversation'),
    path('recent/', get_recent_messages, name='recent_messages'),

    path('notifications/', get_notifications, name='notifications'),

    path('contacts/', get_contacts, name='my_contacts')

]
