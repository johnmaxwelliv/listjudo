from django.db import models
from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode
from django.template import RequestContext
import random

class user_action(models.Model):
    # Reference is here:
    # http://docs.djangoproject.com/en/1.2/ref/request-response/#attributes
    # Later on, this class will probably also have a field for the id of the
    # proto_user that completed the action.
    # POLISH
    # As of 2010-7-22, ratings are not subclassed from user_action, but they
    # probably should be.
    created = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)
    referer = models.URLField(blank=True, null=True, editable=False)
    user_agent = models.CharField(max_length=200, blank=True, null=True, editable=False)
    ip = models.IPAddressField(blank=True, null=True, editable=False)
    absolute_uri = models.URLField(blank=True, null=True, editable=False)
    is_secure = models.NullBooleanField(blank=True, editable=False)
    is_ajax = models.NullBooleanField(blank=True, editable=False)
    def record_request(self, request):
        header = {
            'referer': 'HTTP_REFERER',
            'user_agent': 'HTTP_USER_AGENT',
            'ip': 'REMOTE_ADDR',
        }
        for field in header:
            try:
                setattr(self, field, request.META[header[field]])
            except KeyError:
                pass
        self.absolute_uri = request.build_absolute_uri()
        self.is_secure = request.is_secure()
        self.is_ajax = request.is_ajax()

class UGC(user_action):  # UGC is an acronym for "User Generated Content"
    nickname = models.CharField('your nickname', max_length=20)
    email = models.EmailField("your email (won't be shared)")
    censored = models.BooleanField(default=False)

alphanumbers = '1234567890qwertyuiopasdfghjklzxcvbnm'
def generate_secret_id(n):
    return ''.join([random.choice(alphanumbers) for i in range(n)])

class List(UGC):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    access_code = models.CharField(default=generate_secret_id(8), max_length=8, editable=False)
    admin_code = models.CharField(default=generate_secret_id(8), max_length=8, editable=False)
    views = models.PositiveIntegerField(default=0, editable=False)
    def __unicode__(self):
        return self.title

class Entry(UGC):
    title = models.CharField(max_length=200)
    description = models.TextField()
    list = models.ForeignKey(List)
    rating = RatingField(range=5, can_change_vote=True, allow_anonymous=True)
    oembed = models.URLField(max_length=200, blank=True, null=True, help_text='flickr')
    def __unicode__(self):
        return self.title
    def html(self, request):
        return EntryNode(self).render(RequestContext(request, {}))
