from django.views.generic.simple import direct_to_template as template
from my.lists.models import *

def list(request):
    return template(request, 'lists/list_list.html', {
        'objects': List.objects.all(),
        'request': request,
    })

def detail(request, object_id):
    return template(request, 'lists/list_detail.html', {
        'object': List.objects.get(id=object_id),
        'request': request,
    })
