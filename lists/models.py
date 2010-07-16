from django.db import models
from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode
from django.template import Context

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
    def html(self, request):
        return EntryNode(self).render(Context({'request': request}))
