from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tutorials/', views.tutorials, name='tutorial_list'),
    path('news/', views.news, name='news_list'),
    path('strategies/', views.strategies, name='strategy_list'),
    path('lunar-data/', views.lunar_data_view, name='lunar_data'),
]
