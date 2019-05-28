from django.urls import path

from . import views

event_create = views.EventsViewSet.as_view({'post':'create'})
event_destroy = views.EventsViewSet.as_view({'get':'delete'})
event_update = views.EventsViewSet.as_view({'post':'update'})
event_info = views.EventsViewSet.as_view({'get':'event_info'})
event_close = views.EventsViewSet.as_view({'get':'close_event'})
event_start = views.EventsViewSet.as_view({'get':'start_event'})
event_reopen = views.EventsViewSet.as_view({'get':'reopen_event'})
my_events = views.EventsViewSet.as_view({'get':'my_events'})
add_idea = views.EventsViewSet.as_view({'post':'add_idea'})
update_idea = views.EventsViewSet.as_view({'post':'update_idea'})
list_ideas = views.EventsViewSet.as_view({'get':'list_event_ideas'})
add_comment = views.EventsViewSet.as_view({'post':'add_comment'})
quit_event = views.EventsViewSet.as_view({'get':'quit_event'})
rate_idea = views.EventsViewSet.as_view({'post':'rate_idea'})
add_participants = views.EventsViewSet.as_view({'post':'add_participants'})
remove_participants = views.EventsViewSet.as_view({'post':'remove_participants'})
list_participants = views.EventsViewSet.as_view({'get':'event_participants'})

urlpatterns = [
    path('create/', event_create, name='event_create'),
    path('<int:pk>/destroy/', event_destroy, name='event_destroy'),
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/info/', event_info, name='event_info'),
    path('<int:pk>/close/', event_close, name='event_close'),
    path('<int:pk>/start/', event_start, name='event_start'),
    path('<int:pk>/reopen/', event_reopen, name='event_reopen'),
    path('my-events/', my_events, name='my_events'),
    path('add-idea/', add_idea, name='add_idea'),
    path('<int:pk>/list-ideas/', list_ideas, name='list_ideas'),
    path('update-idea/<int:pk>', update_idea, name='update_idea'),
    path('add-comment/', add_comment, name='add_comment'),
    path('<int:pk>/quit/', quit_event, name='quit_event'),
    path('rate-idea/<int:pk>', rate_idea, name='rate_idea'),
    path('<int:pk>/add-participants/', add_participants, name='add_participants'),
    path('<int:pk>/remove-participants/', remove_participants, name='remove_participants'),
    path('<int:pk>/list-participants/', list_participants, name='list_participants')
]
