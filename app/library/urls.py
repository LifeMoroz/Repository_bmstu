from django.urls import re_path, path

from . import views

app_name = 'library'

urlpatterns = [
    re_path('gain_access/(?P<ct_id>\d+)/', views.GainAccess.as_view(), name='gain_access'),
    path('list/', views.CategoryList.as_view(), name='categories_list'),
]
