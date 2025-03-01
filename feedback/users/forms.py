from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',  'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if login and password:
            user = authenticate(username=login, password=password)

            if not user:
                raise forms.ValidationError("Неверное имя пользователя или пароль.")

            cleaned_data['user'] = user

        return cleaned_data