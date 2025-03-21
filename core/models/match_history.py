from django.db import models

class ScoreInfo(models.Model):
    match_uid = models.CharField(max_length=255, null=True, default=None)
    score = models.IntegerField()
    score_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Score: {self.score}, Info: {self.score_info}"

class Player(models.Model):
    player_uid = models.CharField(max_length=255,  null=False)
    name = models.CharField(max_length=255, null=True, default=None)
    level = models.CharField(max_length=255, default=0)
    def __str__(self):
        return f"Player {self.player_uid}"
    
    
class PlayerStats(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Player {self.player_uid}"
    
class IsWin(models.Model):
    score = models.IntegerField(default=0)
    is_win = models.BooleanField(default=False)

    def __str__(self):
        return f"Score: {self.score}, Win: {self.is_win}"

class MatchPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    assists = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    is_win = models.ForeignKey(IsWin, on_delete=models.CASCADE)  # Linking to the IsWin model

    def __str__(self):
        return f"Player {self.player.player_uid} - Assists: {self.assists}, Kills: {self.kills}, Deaths: {self.deaths}"

class MatchHistory(models.Model):
    match_map_id = models.IntegerField()
    map_thumbnail = models.CharField(max_length=255)
    match_play_duration = models.CharField(max_length=100)
    match_season = models.FloatField()
    match_uid = models.CharField(max_length=255)
    match_winner_side = models.IntegerField()
    mvp_uid = models.CharField(max_length=255)
    svp_uid = models.CharField(max_length=255)
    score_info = models.ForeignKey(ScoreInfo, on_delete=models.CASCADE)
    match_time_stamp = models.BigIntegerField()
    play_mode_id = models.IntegerField()
    game_mode_id = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, default=None)
#    match_player = models.ForeignKey(MatchPlayer, on_delete=models.CASCADE)
    player_hero = models.ForeignKey('Hero', on_delete=models.CASCADE, null=True, default=None)
    camp = models.IntegerField(null=True, blank=True, default=0)
    disconnected = models.BooleanField(default=False)
    def __str__(self):
        return f"Match {self.match_uid} - Winner: {self.match_winner_side}"