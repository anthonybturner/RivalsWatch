from django.shortcuts import render, get_object_or_404
from .models import News, Tutorial, Strategy, Hero, DeveloperDiary, PlayerStats, MatchHistory, MatchesPlayer
from .services.lunarapi import get_lunar_data

def home(request):
    # Fetch latest news, tutorials, strategies
    news = News.objects.all().order_by('-published_at')[:3]  # Most recent 3 news articles
    dev_diaries = DeveloperDiary.objects.all().order_by('-date') [:5] # Most recent 3 news articles
    tutorials = Tutorial.objects.all()[:5]  # Latest 3 tutorials
    strategies = Strategy.objects.all()[:5]  # Latest 3 strategies
   # lunar_data = get_lunar_data('moonphase')  # Example API data

    context = {
        'news': news,
        'dev_diaries': dev_diaries,
        'tutorials': tutorials,
        'strategies': strategies,
    }
    return render(request, 'index.html', context)

def hero(request):
    # Fetch hero data
    heroes = Hero.objects.all().order_by('name')
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

def player_stats(request):
    player_stats = PlayerStats.objects.all()  # Get all player stats
    return render(request, 'player_stats.html', {'player_stats': player_stats})

def match_history(request):
    match_history = MatchHistory.objects.prefetch_related('match_details').all()  # Fetch all matches with details
    return render(request, 'match_history.html', {'match_history': match_history})

def match_history_details(request, match_uid):
    match = get_object_or_404(MatchHistory.objects.prefetch_related('match_details'), match_uid=match_uid)
    players = match.match_details.match_players.all().order_by('-is_win')

    for player in players:
        print(player)
        
    return render(request, 'match_history_details.html', {'players': players})