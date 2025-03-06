from django.db import models

class DeveloperDiary(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit primary key for Hero
    title = models.CharField(max_length=255, unique=True)  # Add 'unique=True'
    date = models.DateField(auto_now_add=True)
    overview = models.TextField()
    image_path = models.CharField(max_length=200)
    full_content = models.TextField()
    
    def __str__(self):
        return self.title
