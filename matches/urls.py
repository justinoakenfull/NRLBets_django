from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.AddMatch, name='add_match'),
    path('matches/', views.upcomingMatches, name='matches'),
    path('complete/', views.completeMatch, name='complete_match'),
]