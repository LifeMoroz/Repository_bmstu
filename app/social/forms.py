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
        widget=forms.RadioSelect(), choices=((False, 'Женский'), (True, 'Мужской'))
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['gender'].initial = kwargs['instance'].gender

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'position', 'email', 'password1', 'password2', 'gender')


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


class SettingsForm(SignUpForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
        initial='',
    )
    password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
        required=False,
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль ещё раз'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'position', 'email', 'gender', 'old_password', 'password1', 'password2', 'id')


class MyForm(SettingsForm):
    old_password = None
    password1 = None
    password2 = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self:
            field.field.disabled = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'position', 'email', 'gender', 'id')
