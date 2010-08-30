from django.conf.urls.defaults import *
from my.lists.models import List

urlpatterns = patterns('my.lists.views',
    (r'^$', 'index'),
    (r'^(?P<object_id>\d+)/$', 'detail', {}, 'published_access'),
    (r'^(?P<object_id>\d+)/add/$', 'add_entry'),
    (r'^(?P<object_id>\d+)/comment/$', 'add_comment'),
    (r'^(?P<object_id>\d+)/(?P<access_code>\w{8})/$', 'detail', {}, 'unpublished_access'),
    (r'^(?P<object_id>\d+)/(?P<access_code>\w{8})/publish/$', 'publish'),
    (r'^create/$', 'create'),
)
