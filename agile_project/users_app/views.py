from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
# Create your views here.
from .models import User
from .serializers import UserSerializer
from .permissions import AuthorOnly


class HomeView(APIView):
    permission_classes = (IsAuthenticated, AuthorOnly)
    def get(self, request):
        content = {'message':'HOME VIEW'}
        return Response(content)



class RegisterView(APIView):

    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.create(request.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
