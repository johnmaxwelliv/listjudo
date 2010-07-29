from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    (r'^lists/', include('my.lists.urls')),
    (r'^ajax_validate/', include('my.ajax_validate.urls')),
    (r'^rate/', include('my.djangoratings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/johniv/Dropbox/li/static/site_media/'}),
    (r'^$', lambda request: HttpResponseRedirect('/lists/')),
)
