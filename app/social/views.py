from django.contrib.auth import logout, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from app.social.forms import SignUpForm, SignInForm
from app.social.models import User


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index:main')


class SignUp(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return {'form': SignUpForm()}

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
        return self.render_to_response({'form': form})


class SignIn(TemplateView):
    template_name = 'signin.html'

    def get_context_data(self, **kwargs):
        return {'form': SignInForm()}

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

            if not user or not check_password(password, user.password):
                form.add_error(NON_FIELD_ERRORS, 'Ошибка авторизации')
                return self.render_to_response({'form': form})

            login(request, user)
            return redirect('index:main')

        return self.render_to_response({'form': form})


class My(View):
    def get(self, request):
        return super().render(request, 'page.html', {})


class UserList(TemplateView):
    template_name = 'user_list.html'
    queryset = User.objects.all()

    def get_queryset(self, queryset):
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(first_name__contains=query)|Q(last_name__contains=query))
        group_id = self.request.GET.get('group_id')
        if group_id:
            queryset = queryset.filter(groups__id=group_id)
        return queryset

    def get_context_data(self, **kwargs):
        return {
            'object_list': self.get_queryset(self.queryset),
            'groups': Group.objects.all()
        }
