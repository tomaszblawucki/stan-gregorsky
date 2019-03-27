from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated

from .serializers import NoteSerializer
from .models import Note

# Create your views here.
class CreateNote(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        print(request.user)
        request.data['attachments'] = None
        serialized = NoteSerializer(data=request.data)
        if serialized.is_valid():
            serialized.create(request.user, request.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class ListNotes(viewsets.ViewSet):
    # serializer_class=NoteSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Note.objects.filter(owner=self.request.user).all()
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Note.objects.all()
        note = get_object_or_404(queryset, pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def update(self, request, pk=None):
        print('UPDATE')
        return Response({'message':'Note updated successfuly'},
                          status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        print('DELETE')
        return Response({'message':'Note deleted'},
                          status=status.HTTP_200_OK)
