from django.urls import path

from . import views


tasks_list = views.ListTasks.as_view({'get':'list'})
task_details = views.ListTasks.as_view({'get':'retrieve'})
task_update = views.ListTasks.as_view({'post':'update'})
task_delete = views.ListTasks.as_view({'get':'destroy'})


urlpatterns = [
    path('create-task/', views.CreateTask.as_view(), name='create_task'),
    path('list-tasks/', tasks_list, name='list_tasks'),
    path('list-tasks/<int:pk>/', task_details, name='task_detail'),
    path('list-tasks/<int:pk>/update/', task_update, name='task_update'),
    path('list-tasks/<int:pk>/destroy/', task_delete, name='task_destroy'),
]
