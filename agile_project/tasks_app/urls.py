from django.urls import path

from . import views


tasks_list = views.ListTasks.as_view({'get':'list'})
task_details = views.ListTasks.as_view({'get':'retrieve'})
task_update = views.ListTasks.as_view({'post':'update'})
task_delete = views.ListTasks.as_view({'get':'destroy'})
task_change_status = views.ListTasks.as_view({'post':'change_status'})
task_assign_user = views.ListTasks.as_view({'post':'assign_to_user'})
task_assign_to_group = views.ListTasks.as_view({'post':'assign_to_group'})

urlpatterns = [
    path('create/', views.CreateTask.as_view(), name='create_task'),
    path('', tasks_list, name='list_tasks'),
    path('<int:pk>/', task_details, name='task_detail'),
    path('<int:pk>/update/', task_update, name='task_update'),
    path('<int:pk>/destroy/', task_delete, name='task_destroy'),
    path('<int:pk>/change-status/', task_change_status, name='task_change_status'),
    path('<int:pk>/assign-user/', task_assign_user, name='task_assign_user'),
    path('<int:pk>/assign-to-group/', task_assign_to_group, name='task_assign_to_group')
]
