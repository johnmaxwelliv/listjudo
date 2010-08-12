from django.db import models
from django.template import RequestContext

from djangoratings.fields import RatingField
from my.lists.templatetags.lists_tags import EntryNode, CommentNode
from imagekit.models import ImageModel
from my.settings import logger

import random

class UserAction(models.Model):
    # Reference is here:
    # http://docs.djangoproject.com/en/1.2/ref/request-response/#attributes
    # Later on, this class will probably also have a field for the id of the
    # proto_user that completed the action.
    # POLISH
    # As of 2010-7-22, ratings are not subclassed from UserAction, but they
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
        '''Save data about the request for the sake of the curious admin, and maybe spam detection type stuff'''
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

class UGC(UserAction):
    '''UGC is an acronym for "User-Generated Content"'''
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
    description = models.TextField(blank=True)
    list = models.ForeignKey(List)
    rating = RatingField(range=5, can_change_vote=True, allow_anonymous=True)
    embed_url = models.URLField('Image/Video URL', verify_exists=True, blank=True, null=True,
        help_text="Video URLs from Youtube and almost all other major video sites are supported.<br />Image URLs should be direct, as in http://www.example.com/photo.jpg<br />If you'd like to use an image that's on your computer, you can upload it to <a href=\"http://imgur.com/\">imgur.com</a> and paste in its \"direct link\".",
    )
    image = models.ForeignKey('EntryImage', blank=True, null=True)

    def __unicode__(self):
        return self.title

    def html(self, request):
        return EntryNode(self).render(RequestContext(request, {}))
        # We need RequestContext so we can provide the csrf_token for the entry's rating form

class EntryImage(ImageModel):
    '''An uploaded image associated with an entry'''
    # ImageKit docs here: http://bitbucket.org/jdriscoll/django-imagekit/wiki/Home
    source_url = models.URLField(editable=False)
    alt = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='public/uploads/%Y/%m/%d')
    num_views = models.PositiveIntegerField(editable=False, default=0)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'lists.entry_image_specs'
        cache_dir = 'public/v1'
        image_field = 'original_image'
        save_count_as = 'num_views'

class ListComment(UGC):
    body = models.TextField()
    list = models.ForeignKey(List)

    def __unicode__(self):
        if len(self.body) > 15:
            return self.body[:15]
        else:
            return self.body

    def html(self, request):
        return CommentNode(self).render(RequestContext(request, {}))
        # No particular need to pass RequestContext here
