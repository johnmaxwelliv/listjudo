from annoying.decorators import JsonResponse
from django.views.generic.simple import direct_to_template as template
from django.db.models import *
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from lists.models import *
from lists.forms import *

def all_lists():
    return List.objects.filter(
            published=True,
        ).filter(
            censored=False,
        )

def featured_lists():
    return List.objects.filter(
            published=True,
        ).filter(
            censored=False,
        ).filter(
            featured=True,
        )

def index(request):
    return template(request, 'lists/list_home.html', {
        'all_lists': Paginator(all_lists(), 4).page(1),
        'featured_lists': Paginator(featured_lists(), 4).page(1),
     })

def create(request):
    '''Create a list'''
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            # POLISH: Optimize 'path' and 'domain' kwargs of set_cookie for minimum HTTP load
            list = form.save(commit=False)
            list.record_request(request)
            list.save()
            result = HttpResponseRedirect('/lists/%d/%s/?admin_code=%s' % \
                (list.id, list.access_code, list.admin_code))
            # The following cookies weren't being set properly.
#            result.set_cookie('nickname', value=list.nickname, max_age=157680000,
#                expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
#            result.set_cookie('email', value=list.email, max_age=157680000,
#                expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
            return result
    else:
        form = None

    empty_list(request=request)

    return template(request, "lists/list_create.html", {
        'form': ListForm(instance=(form or empty_list(request=request))),
    })

def detail(request, object_id, access_code=None):
    '''View a (possibly unpublished) list'''
    list = get_object_or_404(List, pk=object_id)
    if not list.published and access_code != list.access_code:
        return HttpResponseForbidden()
    if list.censored:
        # This should probably be an HttpResponseGone
        # but we'll leave it this way since this is a common access case
        # and it'll be nice to be able to use our standard 404 page
        raise Http404
    list.views = F('views') + 1
    list.save()

    # Get uncensored entries and sort them by average rating
    entries = list.entry_set.filter(
        censored=False,
    )
    entries = entries.extra(select={
        'sophisticated_rating': \
        '((100/%s*rating_score/(rating_votes+%s))+100)/2' % \
        (Entry.rating.range, Entry.rating.weight),
    })
    entries = entries.order_by('-sophisticated_rating')

    comments = list.listcomment_set.filter(
        censored=False,
    )

    # Determine if the user is the list's adminstrator
    # As of 2010-8-6, the only adminstrator privilege is publishing the list
    try:
        admin_code = request.GET['admin_code']
    except (AttributeError, KeyError):
        admin_code = None
    if admin_code == list.admin_code:
        admin_access = True
    else:
        admin_access = False

    return template(request, 'lists/list_detail.html', {
        'list': list,
        'entries': entries,
        'comments': comments,
        'entry_form': EntryForm(instance=empty_entry(list, request=request)),
        'comment_form': CommentForm(instance=empty_comment(list, request=request)),
        'admin_access': admin_access,
        'show_comment_form': comments or not admin_access
        # we don't show the comment form to the admin if there are no comments
        # because then they might confuse it with the form for adding entries
    })

def empty_list(request):
    '''Generate a list object preinitialized with user data'''
    kwargs = retrieve_user_data(request)
    return List(**kwargs)

def empty_entry(list, request):
    '''Generate an entry object preinitialized with user data and a list reference'''
    kwargs = retrieve_user_data(request)
    kwargs['list'] = list
    return Entry(**kwargs)

def empty_comment(list, request):
    '''Generate a comment object preinitialized with user data and a list reference'''
    kwargs = retrieve_user_data(request)
    kwargs['list'] = list
    return ListComment(**kwargs)

def retrieve_user_data(request):
    result = {}
    keys = ('nickname', 'email')
    for key in keys:
        try:
            result[key] = request.COOKIES[key]
        except (AttributeError, KeyError):
            pass
    return result

def add_entry(request, object_id):
    '''Add an entry to a list and return the new entry's id and html.  Called asynchronously.'''
    form = EntryForm(request.POST)
    # our ajax validation should have ensured that the form was valid
    assert form.is_valid()
    entry = form.save(commit=False)
    # save miscelleneous request data for the curious adminstrator's sake
    entry.record_request(request)
    entry.prepare_embeds()
    entry.save()
    result = JsonResponse({
        'id': entry.id,
        'html': entry.html(request, hidden=True),
    })
    # POLISH
    # Calculate the "expires" argument programmatically, or we're screwed
    # when 2068 rolls around.
    result.set_cookie('nickname', value=entry.nickname, max_age=157680000,
        expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
    result.set_cookie('email', value=entry.email, max_age=157680000,
        expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
    return result

def add_comment(request, object_id):
    '''Add a comment to a list and return the new comment's html.  Called asynchronously.'''
    form = CommentForm(request.POST)
    # our ajax validation should have ensured that the form was valid
    assert form.is_valid()
    comment = form.save(commit=False)
    # save miscelleneous request data for the curious adminstrator's sake
    comment.record_request(request)
    comment.save()
    result = JsonResponse({
        'id': comment.id,
        'html': comment.html(request),
    })
    # POLISH
    # Calculate the "expires" argument programmatically, or we're screwed
    # when 2068 rolls around.
    result.set_cookie('nickname', value=comment.nickname, max_age=157680000,
        expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
    result.set_cookie('email', value=comment.email, max_age=157680000,
        expires='Mon, 31-Dec-68 10:00:00 GMT', path='/')
    return result

def publish(request, object_id, access_code):
    '''Attempt to make the list with id object_id visible on the home page and other parts of the site'''
    list = get_object_or_404(List, pk=object_id)
    admin_code = None
    if access_code == list.access_code:
        try:
            admin_code = request.POST['admin_code']
        except (AttributeError, KeyError):
            return HttpResponseForbidden()
    if admin_code != list.admin_code:
        return HttpResponseForbidden()
    list.published = True
    list.save()
    return HttpResponseRedirect('/lists/%d/' % list.id)
