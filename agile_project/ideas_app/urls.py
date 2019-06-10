from django.urls import path

from . import views

# router.register('create_note', views.CreateNote, basename='create-notes')

notes_list = views.ListNotes.as_view({'get':'list'})
note_details = views.ListNotes.as_view({'get':'retrieve'})
note_update = views.ListNotes.as_view({'post':'update'})
note_delete = views.ListNotes.as_view({'get':'destroy'})
# router.register(r'', views.ListNotes, basename='list_notes')

# urlpatterns = router.urls

urlpatterns = [
    path('create-note/', views.CreateNote.as_view(), name='create_note'),
    path('list-notes/', notes_list, name='notes_list'),
    path('<int:pk>/', note_details, name='note_details'),
    path('<int:pk>/update/', note_update, name='update_note'),
    path('<int:pk>/destroy/', note_delete, name='delete_note'),
]
