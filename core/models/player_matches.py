from django.db import models

class PlayerMatches(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
