from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    path('user/register/', views.register, name='register'),
    path('user/profile/', views.profile, name='profile'),
]
