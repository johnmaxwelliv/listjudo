from django.views.generic.simple import direct_to_template as template
from my.lists.models import *
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpResponse
import json

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description', 'list']
        widgets = {
            'list': HiddenInput(),
        }

def list(request):
    return template(request, 'lists/list_list.html', {
        'lists': List.objects.all(),
        'request': request,
    })

def detail(request, object_id):
    list = List.objects.get(id=object_id)
    entries = list.entry_set.all()
    entries = entries.extra(select={
        'sophisticated_rating': '((100/%s*rating_score/(rating_votes+%s))+100)/2' % (Entry.rating.range, Entry.rating.weight)
    })
    entries = entries.order_by('-sophisticated_rating')
    empty_entry = Entry(list=list)
    return template(request, 'lists/list_detail.html', {
        'list': list,
        'entries': entries,
        'request': request,
        'form': EntryForm(instance=empty_entry),
    })

def add_entry(request, object_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        entry = form.save()
        return HttpResponse(json.dumps({'entry_id': entry.id, 'html': entry.html(request)}))
    else:
        return HttpResponse("<h1>Bad entry.</h1>")
