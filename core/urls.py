from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('heroes/', views.hero, name='hero_list'),
    path('tutorials/', views.tutorials, name='tutorial_list'),
    path('news/', views.news, name='news_list'),
    path('strategies/', views.strategies, name='strategy_list'),
    path('player_stats/', views.player_stats, name='player_stats'),
]
