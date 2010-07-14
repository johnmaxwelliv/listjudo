from django.views.generic.simple import direct_to_template as template
from my.lists.models import *
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpResponse

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description', 'list']
        widgets = {
            'list': HiddenInput(),
        }

def list(request):
    return template(request, 'lists/list_list.html', {
        'objects': List.objects.all(),
        'request': request,
    })

def detail(request, object_id):
    object = List.objects.get(id=object_id)
    empty_entry = Entry(list=object)
    return template(request, 'lists/list_detail.html', {
        'object': object,
        'request': request,
        'form': EntryForm(instance=empty_entry),
    })

def add_entry(request, object_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("Entry saved.")
    else:
        return HttpResponse("Bad entry.")
