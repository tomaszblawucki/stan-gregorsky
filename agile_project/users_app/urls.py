from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


users_list = views.UsersViewSet.as_view({'get':'list'})
user_personal = views.UsersViewSet.as_view({'get':'get_user_info'})

urlpatterns = [
    path('', views.HomeView.as_view(), name='users_home'),
    path('get-token/', obtain_auth_token, name='get_token_api'),
    path('register/', views.RegisterView.as_view(), name='register_user'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('dummy/', views.DummyView.as_view(), name='dummy'),
    path('list/', users_list, name='users_list'),
    path('personal/', user_personal, name='user_personal')
]
# to login ( obtain token )
# http http://localhost:8000/users/get-token/ username=<email> password=<pass>

# to get some data with auth
# http http://localhost:8000/users/ 'Authorization: Token c4c15f3c192281c6e5bc46a726f80229c220f6f2'

# register
# http http://localhost:8000/users/register/ email=kini2a@gmail.com password='testpassword' name=kinga surname=jarosz birth_date='2000-12-12'

#forgot password
# http http://localhost:8000/users/forgot-password/ username=<user-email>

#reset password
# http http://localhost:8000/users/reset-password/ username=tom@gmail.com code=75532 new_password=haslo12345
