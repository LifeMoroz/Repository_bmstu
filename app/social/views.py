from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from app.social.forms import SignUpForm, SignInForm, SettingsForm, MyForm
from app.social.models import User


class SignOut(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index:main')


class SignUp(TemplateView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs.get('form') or SignUpForm(),
            'title': 'Регистрация',
            'action': reverse('social:signup'),
            'reset': True
        }

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:main')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            user.groups.add(Group.objects.get(name='Читатели'))
            login(request, user)
            return redirect('index:main')
        return self.render_to_response(self.get_context_data(form=form))


class SignIn(TemplateView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        return {'form': kwargs.get('form') or SignInForm(), 'title': 'Войти', 'action': reverse('social:signin')}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:main')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = SignInForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user and check_password(password, user.password):
                login(request, user)
                return redirect('index:main')

            form.add_error(NON_FIELD_ERRORS, 'Ошибка авторизации')

        return self.render_to_response(self.get_context_data(form=form))


class My(TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        form = MyForm(instance=self.request.user)
        return {
            'form': form,
            'editable': False,
            'my': True
        }


class MySettings(TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        return {
            'form': SettingsForm(instance=self.request.user),
            'editable': True
        }

    def post(self, request, *args, **kwargs):
        form = SettingsForm(data=request.POST, instance=request.user)
        if not form.is_valid():
            return self.render_to_response({'form': form})

        if not check_password(form.cleaned_data['old_password'], request.user.password):
            form.add_error(NON_FIELD_ERRORS, 'Старый пароль не верен')
            return self.render_to_response({'form': form})


class UserList(TemplateView):
    template_name = 'user_list.html'
    queryset = User.objects.all()

    def _get_group_ids(self, group_id):
        return range(group_id, 4)

    def get_queryset(self, queryset):
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(first_name__contains=query)|Q(last_name__contains=query))
        group_id = self.request.GET.get('group_id')
        if group_id:
            queryset = queryset.filter(groups__id__in=group_id)
        return queryset

    def get_context_data(self, **kwargs):
        group = None
        if self.request.GET.get('group_id'):
            try:
                group = Group.objects.get(id=self.request.GET.get('group_id'))
            except Group.DoesNotExist:
                pass
        return {
            'object_list': self.get_queryset(self.queryset),
            'groups': Group.objects.all(),
            'group': group,
        }


class UserView(TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        form = MyForm(instance=user)
        return {
            'user': user,
            'form': form,
            'editable': False
        }
