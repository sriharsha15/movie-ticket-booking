from django.db import models

# Create your models here.
from django.db import models


class ItemCount(models.Model):
    total_count = models.IntegerField(default=250)

    def __unicode__(self):
        return str(self.total_count)


class Video(models.Model):
    video_rank = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    hover_text = models.CharField(max_length=255)
    movie_url = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    rating = models.CharField(max_length=255)
    no_of_votes = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

