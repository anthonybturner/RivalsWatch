from django.db import models
from .player import Player


class GameMode(models.Model):
    game_mode_id = models.IntegerField(unique=True)
    game_mode_name = models.CharField(max_length=255)

class Match(models.Model):
    match_uid = models.CharField(max_length=255, unique=True)
    game_mode = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    replay_id = models.CharField(max_length=255)
    mvp_uid = models.BigIntegerField()
    mvp_hero_id = models.IntegerField()
    svp_uid = models.BigIntegerField()
    svp_hero_id = models.IntegerField()

class MatchPlayer(models.Model):
    match = models.ForeignKey(Match, related_name='match_players', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=255)
    player_icon = models.IntegerField()
    camp = models.IntegerField()
    cur_hero_id = models.IntegerField()
    cur_hero_icon = models.CharField(max_length=255)
    is_win = models.BooleanField(default=False)
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    total_hero_damage = models.FloatField()
    total_hero_heal = models.FloatField()
    total_damage_taken = models.FloatField()

class Badge(models.Model):
    match_player = models.ForeignKey(MatchPlayer, related_name='badges', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    badge_id = models.IntegerField()
    count = models.IntegerField()

class MatchPlayerHero(models.Model):
    match_player = models.ForeignKey(MatchPlayer, related_name='player_heroes', on_delete=models.CASCADE)
    hero_id = models.IntegerField()
    play_time = models.FloatField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    session_hit_rate = models.FloatField()
    hero_icon = models.CharField(max_length=255)