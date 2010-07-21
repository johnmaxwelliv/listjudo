from django.db import models
from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode
from django.template import Context
import random

alphanumeric = '1234567890qwertyuiopasdfghjklzxcvbnm'
def generate_secret_id(n):
    return ''.join([random.choice(alphanumeric) for i in range(n)])

class List(models.Model):
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    secret_id = models.CharField(max_length=10)
    def __unicode__(self):
        return self.title
    def __init__(self, *args, **kwargs):
        self.secret_id = generate_secret_id(10)
        super(List, self).__init__(*args, **kwargs)

class Entry(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    list = models.ForeignKey(List)
    rating = RatingField(range=5, weight=5, can_change_vote=True)
    def __unicode__(self):
        return self.title
    def html(self, request):
        return EntryNode(self).render(Context({'request': request}))
