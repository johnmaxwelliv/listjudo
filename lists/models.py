from django.db import models
from djangoratings.fields import RatingField

class List(models.Model):
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.title

class Entry(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    list = models.ForeignKey(List)
    rating = RatingField(range=5, weight=5, can_change_vote=True)
    def __unicode__(self):
        return self.title
