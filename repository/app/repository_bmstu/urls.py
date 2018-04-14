"""rss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from repository.app.repository_bmstu import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('', views.MainPage.as_view(), name='main_page'),
    path('signup', views.RegView.as_view(), name='signup_url'),
    path('login', views.LogView.as_view(), name='login_url'),
    path('page', views.MyPageView.as_view(), name='page_url'),
    path('users',views.Users.as_view(), name='users_url')
]