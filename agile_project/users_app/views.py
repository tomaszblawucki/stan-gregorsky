# users app views
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import User, ResetPasswordToken
from .serializers import UserSerializer
from .permissions import AuthorOnly

from random import randint
from datetime import datetime
import pytz

utc =pytz.UTC


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

class ForgotPasswordView(APIView):

    def post(self, request):
        '''
        method gets email of user ant checks if it's valid, then sends email with one_shot password
        '''
        # print('='*20, '\n', request)
        # print('\n', request.__dict__)
        # print('\n', request.data)
        # print(dir(request))
        try:
            email = request.data['username']
        except:
            return Response({'message':'invalid email'})

        if User.objects.filter(email=email).exists():

            reset_token = randint(10000, 99999)
            try:
                send_mail(
                    'Your reset password token',
                    f'Please go to your application and assign new password to your account {reset_token}',
                    'agile_app@company.com',
                    ['italo.doc@cowstore.org'],# change to user email-username
                    fail_silently=False)
                token_obj = ResetPasswordToken(email=email, token=reset_token)
                token_obj.save()
                return Response({'message':f'email with temporary password was sent to {request.data["username"]}'})
            except:
                return Response({'error':'internal error during email send process'})
        else:
            return Response({'message':'user with specified email not found in system'})

class ResetPasswordView(APIView):
# http http://localhost:8000/users/reset-password/ username=tom@gmail.com code=75532 new_password=haslo12345

    def post(self, request):
        '''
        method for reset user password by getting token_code, email and new password
        '''
        try:
            token_obj = ResetPasswordToken.objects.filter(
                email=request.data['username'],
                token=request.data['code']).get()
            if token_obj.expire_date >= utc.localize(datetime.now()):
                try:
                    user = User.objects.get(email=request.data['username'])
                    print(user.password)
                    user.set_password(request.data['new_password'])
                    user.save()
                    print(user.password)
                    return Response({'message':'Password changed successfully!'})
                except Exception as e:
                    return Response({'error': f'{e}'})
            else:
                return Response({'error':'Reset code has expired'})


        except ObjectDoesNotExist:
            return Response({'error':'Invalid reset code'})
        except MultipleObjectsReturned:
            return Response({'error':'Internal Server Error'})


class DummyView(APIView):

    def get(self, requeest):
        content = {'message': 'Siergiej działa!'}
        return Response(content)
