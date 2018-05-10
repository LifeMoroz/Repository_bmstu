from django.urls import re_path, path

from . import views

app_name = 'library'

urlpatterns = [
    re_path('gain_access/(?P<ct_id>\d+)/', views.GainAccess.as_view(), name='gain_access'),
    path('list/', views.CategoryList.as_view(), name='categories_list'),
    path('add/', views.CategoryAdd.as_view(), name='add_category'),
    re_path('remove/(?P<ct_id>\d+)/', views.CategoryRemove.as_view(), name='remove'),
]
