from django.urls import path
from . import views


app_name = 'social'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('signout/', views.SignOut.as_view(), name='signout'),

    path('my/', views.My.as_view(), name='my'),
    path('settings/', views.MySettings.as_view(), name='settings'),
    path('list/', views.UserList.as_view(), name='users_list'),
    path('settings/', views.UserList.as_view(), name='users_list'),
]
