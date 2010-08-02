from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.http import HttpResponseRedirect

from my.settings import PROJECT_PATH, DEBUG

urlpatterns = patterns('',
    (r'^lists/', include('my.lists.urls')),
    (r'^ajax_validate/', include('my.ajax_validate.urls')),
    (r'^rate/', include('my.djangoratings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', lambda request: HttpResponseRedirect('/lists/')),
)

if DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': PROJECT_PATH + 'static/site_media/'}),
    )
