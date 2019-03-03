from django.http import HttpResponse

# Create your views here.


def homeView(req):
    return HttpResponse('users list')
