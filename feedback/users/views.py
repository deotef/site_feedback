import logging

from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import Role, CustomUser

logger = logging.getLogger('users')


def ShowRoles(request):
    roles = Role.objects.all()
    return render(request, 'users/show_role.html', {'roles': roles})

def ShowProfile(request, user_id):
    users = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/show_profile.html', {'user' : users})

def CustomUserRegistration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/login.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})

def CustomUserLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            id = user.pk
            return redirect(reverse('profile', args=[id]))
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})