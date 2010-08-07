from django.conf.urls.defaults import *
from my.lists.forms import *

urlpatterns = patterns('ajax_validation.views',
    # (r'^SOME/URL/$', 'ajax_validation.views.validate', {'form_class': ContactForm}, 'contact_form_validate')
    (r'^entry_form/$', 'validate', {'form_class': EntryForm}, 'entry_form_validate'),
    (r'^list_form/$', 'validate', {'form_class': ListForm}, 'list_form_validate'),
    (r'^comment_form/$', 'validate', {'form_class': CommentForm}, 'comment_form_validate'),
)
