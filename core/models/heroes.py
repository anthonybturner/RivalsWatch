from django.db import models

class Hero(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name
