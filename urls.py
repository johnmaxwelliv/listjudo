from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    (r'^lists/', include('my.lists.urls')),
    # (r'^rate/', include('my.djangoratings.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', lambda request: HttpResponseRedirect('/lists/')),
)
