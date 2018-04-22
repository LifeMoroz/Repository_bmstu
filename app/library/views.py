from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from app.library.models import UserCategory, Category


class GainAccess(View):
    def get(self, request, ct_id):
        if Category.objects.filter(id=ct_id).exists():
            UserCategory.objects.get_or_create(user=request.user, category_id=ct_id)
        return redirect('index:main')


class CategoryList(TemplateView):
    template_name = 'category_list.html'
    queryset = Category.objects.all()

    def get_queryset(self, queryset):
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__contains=query)
        group_id = self.request.GET.get('group_id')
        if group_id:
            queryset = queryset.filter(groups__id=group_id)
        return queryset

    def get_context_data(self, **kwargs):
        return {
            'object_list': self.get_queryset(self.queryset),
        }


class CategoryRemove(View):
    def get(self, request, ct_id):
        if request.user.is_authenticated:
            Category.objects.filter(id=ct_id).delete()
        return redirect('index:main')
