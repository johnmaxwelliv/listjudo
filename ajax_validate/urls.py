from django.conf.urls.defaults import *
from my.lists.views import *

urlpatterns = patterns('ajax_validation.views',
    # (r'^SOME/URL/$', 'ajax_validation.views.validate', {'form_class': ContactForm}, 'contact_form_validate')
    (r'^entry_form/$', 'validate', {'form_class': EntryForm}, 'entry_form_validate'),
)
