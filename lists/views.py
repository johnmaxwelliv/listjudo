from django.views.generic.simple import direct_to_template as template
from my.lists.models import *
from django.forms import ModelForm
from django.http import HttpResponse

class EntryForm(ModelForm):
    class Meta:
        model = Entry

def list(request):
    return template(request, 'lists/list_list.html', {
        'objects': List.objects.all(),
        'request': request,
    })

def detail(request, object_id):
    return template(request, 'lists/list_detail.html', {
        'object': List.objects.get(id=object_id),
        'request': request,
        'form': EntryForm(),
    })

def add_entry(request, object_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse("Entry saved.")
