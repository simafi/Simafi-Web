from django import template

register = template.Library()


@register.filter
def field_val(obj, name):
    if not name:
        return ''
    return getattr(obj, name, '')
