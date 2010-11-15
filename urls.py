from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import oembed
oembed.autodiscover()

from django.http import HttpResponseRedirect

from settings import DEBUG, MEDIA_ROOT

urlpatterns = patterns('',
    (r'^lists/', include('lists.urls')),
    (r'^ajax_validate/', include('ajax_validate.urls')),
    (r'^rate/', include('djangoratings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', lambda request: HttpResponseRedirect('/lists/')),
)

if DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
        (r'^versioned/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT.child('versioned'), 'show_indexes': True}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT}),
        (r'^versioned/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT + 'versioned/'}),
    )
