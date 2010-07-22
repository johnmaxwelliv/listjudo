from django.views.generic.simple import direct_to_template as template
from my.lists.models import *
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpResponse
import json

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description', 'nickname', 'email', 'list']
        widgets = {
            'list': HiddenInput(),
        }

def list(request):
    return template(request, 'lists/list_list.html', {
        'lists': List.objects.all(),
    })

def blank_entry(request, list):
    kwargs = {'list': list}
    for key in ('nickname', 'email'):
        try:
            kwargs[key] = request.COOKIES[key]
        except KeyError:
            pass
    return Entry(**kwargs)

def detail(request, object_id):
    list = List.objects.get(id=object_id)
    entries = list.entry_set.all()
    entries = entries.extra(select={
        'sophisticated_rating': \
        '((100/%s*rating_score/(rating_votes+%s))+100)/2' % \
        (Entry.rating.range, Entry.rating.weight)
    })
    entries = entries.order_by('-sophisticated_rating')
    return template(request, 'lists/list_detail.html', {
        'list': list,
        'entries': entries,
        'form': EntryForm(instance=blank_entry(request, list)),
    })

def add_entry(request, object_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        entry = form.save()
        entry.record_request(request)
        result = HttpResponse(json.dumps({'entry_id': entry.id,
            'html': entry.html(request)}))
        # POLISH
        # Calculate the "expires" argument programmatically, or we're screwed
        # when 2068 rolls around.
        result.set_cookie('nickname', value=entry.nickname, max_age=157680000,
            expires='Thu, 31-Dec-68 10:00:00 GMT', path='/')
        result.set_cookie('email', value=entry.email, max_age=157680000,
            expires='Thu, 31-Dec-68 10:00:00 GMT', path='/')
        return result
    else:
        return HttpResponse("<h1>Bad entry.</h1>")
