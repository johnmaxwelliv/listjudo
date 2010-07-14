from django.conf.urls.defaults import *
from my.lists.models import List

urlpatterns = patterns('my.lists.views',
    (r'^$', 'list'),
    (r'^(?P<object_id>\d+)/$', 'detail'),
)
