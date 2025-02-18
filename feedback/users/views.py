from django.shortcuts import render
from rest_framework import generics
from users.models import Role, CustomUser
from users.serializers import CustomUserSerializer


def ShowRoles(request):
    roles = Role.objects.all
    return render(request, 'users/show_role.html', {'roles': roles})


class CustomUserAPIList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class =  CustomUserSerializer