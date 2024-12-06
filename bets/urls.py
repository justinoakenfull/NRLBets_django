from django.urls import path, include
from . import views

urlpatterns = [
    path('add', views.add_Bet, name='add_bet')
]