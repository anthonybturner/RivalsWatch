from django.db import models

class ScoreInfo(models.Model):
    score = models.IntegerField()
    score_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Score: {self.score}, Info: {self.score_info}"

class Player(models.Model):
    player_uid = models.CharField(max_length=255)
    assists = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    is_win = models.BooleanField()
    disconnected = models.BooleanField()
    camp = models.CharField(max_length=1)  # 'A' or 'B'
    score_info = models.ForeignKey(ScoreInfo, on_delete=models.CASCADE)
    player_hero = models.ForeignKey('Hero', on_delete=models.CASCADE)  # Link to your existing Hero model

    def __str__(self):
        return f"Player {self.player_uid}"

class MatchHistory(models.Model):
    match_map_id = models.IntegerField()
    map_thumbnail = models.CharField(max_length=255)
    match_play_duration = models.CharField(max_length=100)
    match_season = models.FloatField()
    match_uid = models.CharField(max_length=255)
    match_winner_side = models.CharField(max_length=1)  # 'A' or 'B'
    mvp_uid = models.CharField(max_length=255)
    svp_uid = models.CharField(max_length=255)
    score_info = models.ForeignKey(ScoreInfo, on_delete=models.CASCADE)
    match_time_stamp = models.BigIntegerField()
    play_mode_id = models.IntegerField()
    game_mode_id = models.IntegerField()
    match_player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Match {self.match_uid} - Winner: {self.match_winner_side}"
