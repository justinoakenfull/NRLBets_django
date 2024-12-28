from django.urls import path, include
from . import views

urlpatterns = [
    path('add', views.add_Bet, name='add_bet'),
    path('bets', views.get_current_bets, name='all_user_bets'),
    path('bets/<int:bet_id>/cancel', views.cancel_bet, name='cancel_bet'),
]