from django.http import HttpResponse
from django.shortcuts import render

from main.models import Role


# Create your views here.
def home(request):
    return HttpResponse("Главная страница")


def ShowRoles(request):
    roles = Role.objects.all()
    data = {
        'roles': roles,
    }
    return render(request, 'main/show_role.html', context=data)