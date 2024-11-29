from django.urls import path, include
from . import views

urlpatterns = [
    path('add', views.AddBet, name='add_bet'),
]