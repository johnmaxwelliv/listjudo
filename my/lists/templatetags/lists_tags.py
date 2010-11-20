from django import template
from django.template import loader

register = template.Library()

class EntryNode(template.Node):
    def __init__(self, entry):
        self.entry = entry
        self.template = loader.get_template("lists/entry.html")
        self.cache_period = 2592000  # 30 days in seconds, for cache backend
        # Note that memcached works differently if you give it more than 30 days' worth of seconds, see
        # http://code.google.com/p/memcached/wiki/FAQ#What_are_the_limits_on_setting_expire_time?_%28why_is_there_a_30_d
    def render(self, context):
        # POLISH
        # Potential bug in the making here... what if the context object passed
        # to render has an unexpected 'entry' field later on?
        context['entry'] = self.entry
        context['cache_period'] = self.cache_period
        return self.template.render(context)

class CommentNode(template.Node):
    def __init__(self, comment):
        self.comment = comment
        self.template = loader.get_template("lists/comment.html")
    def render(self, context):
        # POLISH
        # Potential bug in the making here... what if the context object passed
        # to render has an unexpected 'entry' field later on?
        context['comment'] = self.comment
        return self.template.render(context)

@register.simple_tag
def entry_html(entry):
    return EntryNode(entry)

@register.simple_tag
def comment_html(comment):
    return CommentNode(comment)
