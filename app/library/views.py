from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from app.library.forms import CategoryForm
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


class CategoryAdd(TemplateView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs.get('form') or CategoryForm(),
            'title': 'Добавить раздел',
            'action': reverse('library:add_category')
        }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('social:signin')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            obj = form.save(False)
            obj.author = request.user
            obj.save()
            return redirect(reverse('library:add_category') + "?success=1")
        return self.render_to_response(self.get_context_data(form=form))
