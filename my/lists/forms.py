from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from lists.models import *

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

class CommentForm(ModelForm):
    class Meta:
        model = ListComment
        fields = ['body', 'nickname', 'email', 'list']
        widgets = {
            'list': HiddenInput(),
        }
