from lib.djangoratings.models import Vote
from my.lists.models import Entry, List, ListComment

def get(c):
    return c.objects.all()[:]

def s():
    everything = []
    for c in [Vote, Entry, List, ListComment]:
        everything.extend(get(c))
    everything.sort(key=lambda item: item.date_added if type(item) is Vote else
    item.created)
    return everything
