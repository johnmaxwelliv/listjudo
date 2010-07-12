from django.conf.urls.defaults import *
from my.lists.models import List

info_dict = {
    'queryset': List.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$',
        'django.views.generic.list_detail.object_detail', info_dict),
)
