from django.db import models



class Player(models.Model):
    player_uid = models.CharField(max_length=255,  null=False)
    name = models.CharField(max_length=255, null=True, default=None)
    level = models.CharField(max_length=255, default=0)
    def __str__(self):
        return f"Player {self.player_uid}"
    
    
class PlayerHero(models.Model):
    hero_id = models.IntegerField(unique=True)  # Unique identifier for the hero
    hero_name = models.CharField(max_length=100)  # Name of the hero
    hero_type = models.URLField()  # URL to the hero's image or type
    kills = models.IntegerField(default=0)  # Number of kills made by the hero
    deaths = models.IntegerField(default=0)  # Number of deaths the hero has experienced
    assists = models.IntegerField(default=0)  # Number of assists made by the hero
    play_time = models.FloatField()  # Play time of the hero in seconds
    total_hero_damage = models.FloatField()  # Total hero damage dealt
    total_damage_taken = models.FloatField()  # Total damage taken by the hero
    total_hero_heal = models.FloatField(default=0)  # Total healing done by the hero
    
    def __str__(self):
        return self.hero_name
    
    
class PlayerStats(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"Player {self.player_uid}"