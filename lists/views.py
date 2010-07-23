from django.views.generic.simple import direct_to_template as template
from my.lists.models import *
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'description', 'nickname', 'email', 'list']
        widgets = {
            'list': HiddenInput(),
        }

class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'nickname', 'email']

def list(request):
    return template(request, 'lists/list_list.html', {
        'lists': List.objects.filter(
            published=True
        ).filter(
            censored=False
        ),
    })

def blank_entry(list, request=None, instance=None):
    kwargs = retrieve_user_data(request, instance)
    kwargs['list'] = list
    return Entry(**kwargs)

def blank_list(request=None, instance=None):
    kwargs = retrieve_user_data(request, instance)
    return List(**kwargs)

def retrieve_user_data(request=None, instance=None):
    result = {}
    keys = ('nickname', 'email')
    if request:
        for key in keys:
            try:
                result[key] = request.COOKIES[key]
            except AttributeError, KeyError:
                pass
    elif instance:
        for key in keys:
            try:
                result[key] = getattr(instance, key)
            except AttributeError:
                pass
    else:
        raise AssertionError("You must pass one of request or instance to retrieve_user_data.")
    return result

def detail(request, object_id, access_code=None):
    list = get_object_or_404(List, pk=object_id)
    if not list.published and access_code != list.access_code:
        raise Http404
    if list.censored:
        raise Http404
    entries = list.entry_set.filter(
        censored=False
    )
    entries = entries.extra(select={
        'sophisticated_rating': \
        '((100/%s*rating_score/(rating_votes+%s))+100)/2' % \
        (Entry.rating.range, Entry.rating.weight)
    })
    entries = entries.order_by('-sophisticated_rating')
    admin_code = None
    if access_code == list.access_code:
        try:
            admin_code = request.GET['admin_code']
        except (AttributeError, KeyError):
            pass
    if admin_code == list.admin_code:
        admin_access = True
    else:
        admin_access = False
    return template(request, 'lists/list_detail.html', {
        'list': list,
        'entries': entries,
        'form': EntryForm(instance=blank_entry(list, request=request)),
        'admin_access': admin_access,
    })

def add_entry(request, object_id):
    form = EntryForm(request.POST)
    if form.is_valid():
        entry = form.save()
        entry.record_request(request)
        entry.save()
        result = HttpResponse(json.dumps({
            'entry_id': entry.id,
            'html': entry.html(request),
        }))
        # POLISH
        # Calculate the "expires" argument programmatically, or we're screwed
        # when 2068 rolls around.
        result.set_cookie('nickname', value=entry.nickname, max_age=157680000,
            expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
        result.set_cookie('email', value=entry.email, max_age=157680000,
            expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
        return result
    else:
        return HttpResponse("<h1>Bad entry.</h1>")

def create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save()
            list.record_request(request)
            list.save()
            # POLISH: Here and elswhere, do you really need to be saving twice?
            result = HttpResponseRedirect('/lists/%d/%s/?admin_code=%s' % \
                (list.id, list.access_code, list.admin_code))
            result.set_cookie('nickname', value=list.nickname, max_age=157680000,
                expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
            result.set_cookie('email', value=list.email, max_age=157680000,
                expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
            return result

    return template(request, "lists/list_create.html", {
        'form': ListForm(instance=blank_list(request=request)),
    })

def publish(request, object_id, access_code):
    list = get_object_or_404(List, pk=object_id)
    admin_code = None
    if access_code == list.access_code:
        try:
            admin_code = request.POST['admin_code']
        except (AttributeError, KeyError):
            raise Http404
    if admin_code != list.admin_code:
        raise Http404
    list = get_object_or_404(List, pk=object_id)
    list.published = True
    list.save()
    return HttpResponseRedirect('/lists/%d/' % list.id)
