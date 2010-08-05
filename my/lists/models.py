from django.db import models
from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode
from django.template import RequestContext
import random
from imagekit.models import ImageModel
import urllib
import my.settings
import datetime
from django.core.files.storage import default_storage as storage

class Image(ImageModel):
    source = models.URLField(editable=False)
    name = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='uploaded-images/%Y/%m/%d')
    num_views = models.PositiveIntegerField(editable=False, default=0)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'lists.specs'
        cache_dir = 'cached'
        image_field = 'original_image'
        save_count_as = 'num_views'

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
    embed_url = models.URLField(max_length=200, blank=True, null=True,
        verbose_name='Image/Video URL',
        help_text="Video URLs from Youtube and almost all other major video sites are supported.<br />If you'd like to use an image that's on your computer, you can upload it to <a href=\"http://imgur.com/\">imgur.com</a> and paste in its url.",
    )
    image = models.ForeignKey(Image, blank=True, null=True)
    def __unicode__(self):
        return self.title
    def html(self, request):
        return EntryNode(self).render(RequestContext(request, {}))
