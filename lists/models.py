from django.db import models
from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode
from django.template import Context
import random

class user_action(models.Model):
    # Reference is here:
    # http://docs.djangoproject.com/en/1.2/ref/request-response/#attributes
    # Later on, this class will probably also have a field for the id of the
    # proto_user that completed the action.
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    referer = models.URLField(blank=True, null=True)
    user_agent = models.CharField(max_length=200, blank=True, null=True)
    ip = models.IPAddressField(blank=True, null=True)
    absolute_uri = models.URLField(blank=True, null=True)
    is_secure = models.NullBooleanField(blank=True)
    is_ajax = models.NullBooleanField(blank=True)
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

alphanumbers = '1234567890qwertyuiopasdfghjklzxcvbnm'
def generate_secret_id(n):
    return ''.join([random.choice(alphanumbers) for i in range(n)])

class List(UGC):
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    secret_id = models.CharField(default='notasecret', max_length=10)
    views = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return self.title
    def __init__(self, *args, **kwargs):
        self.secret_id = generate_secret_id(10)
        return super(List, self).__init__(*args, **kwargs)

class Entry(UGC):
    title = models.CharField(max_length=200)
    description = models.TextField()
    list = models.ForeignKey(List)
    rating = RatingField(range=5, weight=5, can_change_vote=True,
        allow_anonymous=True)
    def __unicode__(self):
        return self.title
    def html(self, request):
        return EntryNode(self).render(Context({'request': request}))
