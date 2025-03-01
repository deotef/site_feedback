import logging

from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import Role, CustomUser

logger = logging.getLogger('users')


def ShowRoles(request):
    roles = Role.objects.all()
    return render(request, 'users/show_role.html', {'roles': roles})


def ShowProfile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/show_profile.html', {'user' : user})


def CustomUserRegistration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #logger.info('Пользователь зарегистрирован')
            return redirect(reverse('loginform'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form':form})


def CustomUserLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            pk = user.pk
            return redirect(reverse('profile', args=[pk]))
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def home(request):
    return render(request, 'users/home_page.html')

def logout_user(request):
    logout(request)
    return redirect('home')