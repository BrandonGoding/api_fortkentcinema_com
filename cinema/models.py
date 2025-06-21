from django.db import models
from core.mixins import SlugModelMixin

class Film(SlugModelMixin):
    title = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=100, unique=True)
    youtube_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
