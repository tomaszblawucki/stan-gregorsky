from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated

from .serializers import TaskSerializer
from .models import Task, TaskStatus

# Create your views here.
class CreateTask(APIView):
    permission_classes = (IsAuthenticated,)#, ProjectManagerOnly) #is_project_manager)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.user, request.data)
        else:
            return Response({'message':f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Task created'})

class ListTasks(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    # ACTION PERMISSIONS
    def project_manager_only(self, request):
        from users_app.models import UserRoles
        if request.user.role is not UserRoles.MAN:
            raise PermissionDenied()
        return True
    ##############################################

    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        self.project_manager_only(request)
        try:
            task_obj = Task.objects.get(pk=pk)
        except:
            return Response({'message': 'Task not found.'},
                             status=status.HTTP_404_NOT_FOUND)
        if task_obj.creator != request.user:
            return Response({'message':'operation not permitted, only creator can update this task'},
                             status.HTTP_403_FORBIDDEN)
        serializer=TaskSerializer(data=request.data)
        serializer.update(request.data, pk=pk)
        return Response({'message': 'Task updated successfuly'})

    def destroy(self, request, pk=None):
        self.project_manager_only(request)
        try:
            task_obj = Task.objects.get(pk=pk)
        except:
            return Response({'message':'Task not found.'},
                             status=status.HTTP_404_NOT_FOUND)
        if task_obj.creator != request.user:
            return Response({'message':'operation not permitted, only creator can delete this task'},
                             status.HTTP_403_FORBIDDEN)
        try:
            task_obj.delete()
        except:
            return Response({'message':'Error ocured during delete action'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':'Task deleted'},
                          status=status.HTTP_200_OK)

#######################################################################

    def change_status(self, request, pk=None):
        try:
            task_obj = Task.objects.get(pk=pk)
        except:
            return Response({'message': 'Task not found.'},
                             status=status.HTTP_404_NOT_FOUND)
        if task_obj.creator != request.user and task_obj.assigned_user != request.user:
            return Response({'message':'Operation not permitted'},
                             status.HTTP_403_FORBIDDEN)
        items = request.data
        task_status = items.get('task_status', task_obj.status)
        if task_status not in TaskStatus.__members__:
            return Response({'message':'Invalid task status value'}, status=status.HTTP_400_BAD_REQUEST)
        task_obj.status = TaskStatus[task_status]
        task_obj.save()
        return Response({'message': 'Task status updated successfuly'})

    # def assign_to_project(self, request, pk=None):
    #     self.project_manager_only(request)
    #     try:
    #         task_obj = Task.objects.get(pk=pk)
    #     except:
    #         return Response({'message': 'Task not found.'},
    #                          status=status.HTTP_404_NOT_FOUND)
    #     return Response('{message: assign to group}')

    def assign_to_user(self, request, pk=None):
        from users_app.models import User, UserRoles
        try:
            task_obj = Task.objects.get(pk=pk)
        except:
            return Response({'message': 'Task not found.'},
                             status=status.HTTP_404_NOT_FOUND)
        try:
            user_obj = User.objects.get(pk=request.data['user_id'])
        except:
            return Response({'message': 'User not exists.'},
                             status=status.HTTP_404_NOT_FOUND)

        print(request.user.role)
        if task_obj.assigned_user and request.user.role != 'MAN':
            return Response({'Only Project Manager can change person already assigned to task'})
        task_obj.assigned_user = user_obj
        task_obj.save()
        return Response({'message': f'assigned user: {user_obj.pk} to task {task_obj.pk}'})


# resign task view!!
# assign task to project
