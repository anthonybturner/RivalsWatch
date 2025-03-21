from django.urls import path
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', views.home, name='home'),
    path('heroes/', views.hero, name='hero_list'),
    path('tutorials/', views.tutorials, name='tutorial_list'),
    path('news/', views.news, name='news_list'),
    path('strategies/', views.strategies, name='strategy_list'),
    path('player_stats/', views.player_stats, name='player_stats'),
    path('match_history/', views.match_history, name='match_history_list'),
]+ debug_toolbar_urls()
