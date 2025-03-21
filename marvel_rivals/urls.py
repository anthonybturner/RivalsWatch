"""
URL configuration for marvel_rivals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('heroes/', views.hero, name='hero_list'),
    path('news/', views.news, name='news'),
    path('strategies/', views.strategies, name='strategies'),
    path('tutorials/', views.tutorials, name='tutorials'),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('player_stats/', views.player_stats, name='player_stats'),
    path('player_matches/', views.match_history, name='player_matches'),
    path('match_history/', views.match_history, name='match_history_list'),
]
