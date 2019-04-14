from django.urls import path

from . import views

groups_list = views.ProjectGroupView.as_view({'get':'list_my_groups'})#list
# groups_list = views.ProjectGroupView.as_view({'get':'list'})# CHANGE TO LIST_MY_GROUPS
group_create = views.ProjectGroupView.as_view({'post':'create'})
group_update = views.ProjectGroupView.as_view({'post':'update'})
group_close = views.ProjectGroupView.as_view({'get':'close_group'})
group_reopen = views.ProjectGroupView.as_view({'get':'reopen_group'})
group_delete_members = views.ProjectGroupView.as_view({'post':'delete_members'})
group_add_members = views.ProjectGroupView.as_view({'post':'add_members'})
group_details = views.ProjectGroupView.as_view({'get':'retrieve'})

urlpatterns = [
    path('create/', group_create, name='create_group'),
    path('list/', groups_list, name='list_groups'),
    path('<int:pk>/update/', group_update, name='update_group'),
    path('<int:pk>/close/', group_close, name='close_group'),
    path('<int:pk>/reopen/', group_reopen, name='reopen_group'),
    path('<int:pk>/delete_members/', group_delete_members, name='delete_members'),
    path('<int:pk>/add_members/', group_add_members, name='add_members'),
    path('<int:pk>/', group_details, name='group_details')
]
