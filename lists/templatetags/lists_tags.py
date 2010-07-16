from django import template
from django.template import loader

register = template.Library()

class EntryFormNode(template.Node):
    def render(self, context):
        t = loader.get_template("lists/entry_form.html")
        return t.render(context)

class EntryNode(template.Node):
    def __init__(self, entry):
        self.entry = entry
    def render(self, context):
        context['entry'] = self.entry
        t = loader.get_template("lists/entry.html")
        return t.render(context)

@register.tag
def entry_form(parser, token):
    return EntryFormNode()

@register.simple_tag
def entry_html(entry):
    return EntryNode(entry)
