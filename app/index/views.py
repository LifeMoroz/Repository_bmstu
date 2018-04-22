from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.
from django.views.generic import TemplateView

from app.library.constants import Access
from app.library.models import Category, UserCategory


class BaseView(View):
    def render(self, request, template, context):
        context.update({
            'authorized': request.user.is_authenticated,
            'user': {'name': request.user.username},
        })

        return render(request, template, context)


class MainPage(TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        free_catalogs = Category.objects.filter(access=Access.PUBLIC)
        private_catalogs = Category.objects.filter(access=Access.PRIVATE)
        if self.request.user.groups.filter(name='Читатели').exists():
            return {
                'public': free_catalogs,
                'private': private_catalogs,
                'granted': Category.objects.filter(usercategory__granted=True, usercategory__user=self.request.user)
            }
        edit_all = self.request.user.groups.filter(Q(name='Администраторы')|Q(name='Редакторы')).exists()
        return {
            'public': Category.objects.all(),
            'can_delete': Category.objects.all() if edit_all else self.request.user.categories.all()
        }
