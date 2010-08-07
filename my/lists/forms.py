from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from my.lists.models import *

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description', 'nickname', 'email', 'list', 'embed_url']
        widgets = {
            'list': HiddenInput(),
        }

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'nickname', 'email']
