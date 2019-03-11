from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='users_home'),
    path('get-token/', obtain_auth_token, name='get_token_api'),
    path('register/', views.RegisterView.as_view(), name='register_user')
]
# to login ( obtain token )
# http http://localhost:8000/users/get-token/ username=<email> password=<pass>

# to get some data with auth
# http http://localhost:8000/users/ 'Authorization: Token c4c15f3c192281c6e5bc46a726f80229c220f6f2'
