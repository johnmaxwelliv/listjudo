from django import template
from django.template import loader

register = template.Library()

class EntryFormNode(template.Node):
    def __init__(self, form=None):
        self.template = loader.get_template("lists/entry_form.html")
    def render(self, context):
        return self.template.render(context)

class EntryNode(template.Node):
    def __init__(self, entry):
        self.entry = entry
        self.template = loader.get_template("lists/entry.html")
    def render(self, context):
        # POLISH
        # Potential bug in the making here... what if the context object passed
        # to render has an unexpected 'entry' field later on?
        context['entry'] = self.entry
        return self.template.render(context)

@register.tag
def entry_form(parser, token):
    return EntryFormNode()

@register.simple_tag
def entry_html(entry):
    return EntryNode(entry)
