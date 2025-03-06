from django.shortcuts import render
from .models import News, Tutorial, Strategy, Hero
from .services.lunarapi import get_lunar_data

def home(request):
    # Fetch latest news, tutorials, strategies
    news = News.objects.all().order_by('-published_at')[:3]  # Most recent 3 news articles
    tutorials = Tutorial.objects.all()[:3]  # Latest 3 tutorials
    strategies = Strategy.objects.all()[:3]  # Latest 3 strategies
   # lunar_data = get_lunar_data('moonphase')  # Example API data

    context = {
        'news': news,
        'tutorials': tutorials,
        'strategies': strategies,
    }
    return render(request, 'index.html', context)

def hero(request):
    # Fetch hero data
    heroes = Hero.objects.all().order_by('-name')
    context = {
        'heroes': heroes
    }
    return render(request, 'hero.html', context)

# View for displaying the list of tutorials (text and YouTube)
def tutorials(request):
    tutorials = Tutorial.objects.all()  # Get all tutorials from the database
    return render(request, 'tutorials.html', {'tutorials': tutorials})

# View for displaying news articles
def news(request):
    news = News.objects.all().order_by('-published_at')  # Order by published_at descending
    return render(request, 'news.html', {'news': news})

# View for displaying strategies and fundamentals
def strategies(request):
    strategies = Strategy.objects.all()  # Get all strategies
    return render(request, 'strategy.html', {'strategies': strategies})

def lunar_data_view(request):
    endpoint = "moonphase"  # Example endpoint
    lunar_data = get_lunar_data(endpoint)
    return render(request, 'lunar_data.html', {'lunar_data': lunar_data})

