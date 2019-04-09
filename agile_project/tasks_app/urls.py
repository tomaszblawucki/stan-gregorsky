from django.urls import path

from . import views


tasks_list = views.ListTasks.as_view({'get':'list'})
task_details = views.ListTasks.as_view({'get':'retrieve'})
task_update = views.ListTasks.as_view({'post':'update'})
task_delete = views.ListTasks.as_view({'get':'destroy'})
task_change_status = views.ListTasks.as_view({'post':'change_status'})
task_assign_user = views.ListTasks.as_view({'post':'assign_to_user'})

urlpatterns = [
    path('create/', views.CreateTask.as_view(), name='create_task'),
    path('list/', tasks_list, name='list_tasks'),
    path('list/<int:pk>/', task_details, name='task_detail'),
    path('list/<int:pk>/update/', task_update, name='task_update'),
    path('list/<int:pk>/destroy/', task_delete, name='task_destroy'),
    path('list/<int:pk>/change-status/', task_change_status, name='task_change_status'),
    path('list/<int:pk>/assign-user/', task_assign_user, name='task_assign_user'),
]
