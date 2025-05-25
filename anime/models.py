from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class WatchedAnime(models.Model):
    client =models.ForeignKey(User, on_delete=models.CASCADE)
    anilist_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    genre = models.JSONField()
    cover_image = models.URLField()


class Userpreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_genres = models.JSONField()
    notifications_enabled = models.BooleanField(default=True)