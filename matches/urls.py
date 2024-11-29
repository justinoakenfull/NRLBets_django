from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.AddMatch, name='add_match'),
    path('upcoming/', views.upcomingMatches, name='upcoming_matches'),
    path('complete/', views.completeMatch, name='complete_match'),
]