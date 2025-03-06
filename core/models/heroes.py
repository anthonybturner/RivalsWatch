from django.db import models

class Hero(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key for Hero
    name = models.CharField(max_length=255)
    description = models.TextField()
    real_name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    attack_type = models.CharField(max_length=100)
    team = models.JSONField()  # Store the list of teams
    difficulty = models.IntegerField()
    bio = models.TextField()
    lore = models.TextField()

    def __str__(self):
        return self.name

class Transformation(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key for Transformation
    hero = models.ForeignKey(Hero, related_name='transformations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    health = models.CharField(max_length=255)
    movement_speed = models.CharField(max_length=50)
    

    def __str__(self):
        return f'{self.hero.name} - {self.name}'

class Quality(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key for Quality
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    value = models.IntegerField()
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Costume(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key for Costume
    hero = models.ForeignKey(Hero, related_name='costumes', on_delete=models.CASCADE)  # Link to Hero
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    quality_name = models.CharField(max_length=100, default="Unknown")  
    quality_color = models.CharField(max_length=50, default="gray")  
    quality_value = models.IntegerField(default=1)
    quality_icon = models.CharField(max_length=255, default="")  
    description = models.TextField(default="No description available")
    appearance = models.TextField(default="No appearance data available")

    def __str__(self):
        return f'{self.hero.name} - {self.name}'

class Ability(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key
    hero = models.ForeignKey(Hero, related_name='abilities', on_delete=models.CASCADE)  # Link to Hero
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    type = models.CharField(max_length=100, default="Normal")
    is_collab = models.BooleanField(default=False)
    key = models.CharField(max_length=100, default="")
    damage = models.CharField(max_length=300, default="0")
    casting = models.TextField(default="")
    cooldown = models.CharField(max_length=300, default="0s")
    projectile_speed = models.CharField(max_length=150, default="0m/s")

    def __str__(self):
        return f"{self.hero.name} - {self.name}"