from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated

from .serializers import TaskSerializer
from .models import Task, TaskStatus

# Create your views here.
class CreateTask(APIView):
    permission_classes = (IsAuthenticated, ) #is_project_manager)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.user, request.data)
        else:
            return Response({'message':f'{serializer.errors}'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Task created'})

class ListTasks(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        return Response('{message: retrieve}')

    def update(self, request, pk=None):
        queryset = Task.objects.all()
        task_obj = get_object_or_404(queryset, pk=pk)
        serializer=TaskSerializer(data=request.data)
        serializer.update(request.data, pk=pk)

            # return Response({'message':f'{serializer.errors}'})
        return Response('{message: update}')

    def destroy(self, request, pk=None):
        return Response('{message: delete}')

    def change_status(self, request, pk=None):
        return Response('{message: assign status}')

    def assign_to_project(self, request, pk=None):
        return Response('{message: assign to group}')

    def assign_to_user(self, request, pk=None):
        return Response('{message: assign to user}')
