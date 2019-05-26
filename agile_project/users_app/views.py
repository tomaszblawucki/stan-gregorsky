# users app views
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token

from .models import User, ResetPasswordToken
from .serializers import UserSerializer
from .permissions import AuthorOnly

from random import randint
from datetime import datetime
import pytz

utc = pytz.UTC

'''
TO DO:
- Lista wszystkich użytkowników OK
! Lista użytkowników filtrowana po specjalizacji, stażu, grupie itd
- Dane szczegółowe zalogowanego użytkownika OK
- Zaimplementuj AuthToken (ostatnio zalogowano..) https://www.django-rest-framework.org/api-guide/authentication/
'''

class RegisterView(APIView):

    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.create(request.data)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # serializer_class = UserSerializer
    # queryset = User.objects.all()

    def list(self, request):
        queryset = User.objects.all().values('id', 'email', 'name', 'surname', 'role')
        # serializer = UserSerializer(queryset, many=True, allow_null=True)
        # print(serializer.data)
        return Response(queryset)

    def retrieve(self, request):
        return Response('Single User View')

    def get_user_info(self, request):
        # http http://localhost:8000/users/personal/  'Authorization: Token a1b1cc9bff5d523ba578a749b8ee6daaf02e903f'
        current_user = User.objects.defer('password').filter(id=request.user.id).values()
        exclude_fields = ('password',)
        [[d.pop(key, None) for d in current_user] for key in exclude_fields]
        print(current_user)
        return Response(current_user)
    # def retrieve(self, request, pk=None):



class ForgotPasswordView(APIView):

    def post(self, request):
        '''
        method gets email of user ant checks if it's valid, then sends email with one_shot password
        '''
        try:
            email = request.data['username']
        except:
            return Response({'message':'invalid email'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            has_token = False
            token_obj = ResetPasswordToken.objects.filter(email=email,expire_date__gt=utc.localize(datetime.now())).order_by('expire_date')
            if not token_obj.exists():
                reset_token = randint(10000, 99999)
            else:
                reset_token = token_obj[0].token
                print(reset_token)
            try:
                send_mail(
                    'Your reset password token',
                    f'Please go to your application and assign new password to your account {reset_token}',
                    'agile_app@company.com',
                    ['stan.gregorsky@gmail.com'],# change to user email-username
                    fail_silently=False)
                if not has_token:
                    token_obj = ResetPasswordToken(email=email, token=reset_token)
                    token_obj.save()
                return Response({'message':f'email with temporary password was sent to {request.data["username"]}'})
            except:
                return Response({'error':'internal error during email send process'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'user with specified email not found in system'}, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'Reset code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error':'Invalid reset code'})
        except MultipleObjectsReturned:
            return Response({'error':'Internal Server Error'})
