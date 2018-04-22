from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.social.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите имя'}),
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите фамилию'}),
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите email'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль ещё раз'}),
    )
    gender = forms.ChoiceField(
        label='Пол',
        widget=forms.RadioSelect(), choices=((0, 'Женский'), (1, 'Мужской'))
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'gender')


class SignInForm(forms.ModelForm):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите email'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
    )

    class Meta:
        model = User
        fields = ('email', 'password')
