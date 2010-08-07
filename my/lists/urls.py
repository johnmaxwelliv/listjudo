from django.conf.urls.defaults import *
from my.lists.models import List

urlpatterns = patterns('my.lists.views',
    (r'^$', 'index'),
    (r'^(?P<object_id>\d+)/$', 'detail'),
    (r'^(?P<object_id>\d+)/add/$', 'add_entry'),
    (r'^(?P<object_id>\d+)/(?P<access_code>\w{8})/$', 'detail'),
    (r'^(?P<object_id>\d+)/(?P<access_code>\w{8})/publish/$', 'publish'),
    (r'^create/$', 'create'),
)
