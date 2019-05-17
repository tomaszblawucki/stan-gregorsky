from django.urls import path

from . import views

event_create = views.EventsViewSet.as_view({'post':'create'})


urlpatterns = [
    path('create/', event_create, name='event_create')
]
