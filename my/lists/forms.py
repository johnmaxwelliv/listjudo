from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from lists.models import *

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'embed_url', 'description', 'nickname', 'list'] # used to also have 'email'
        widgets = {
            'list': HiddenInput(),
        }

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'nickname'] # used to also have 'email'

class CommentForm(ModelForm):
    class Meta:
        model = ListComment
        fields = ['body', 'nickname', 'list'] # used to also have 'email'
        widgets = {
            'list': HiddenInput(),
        }
