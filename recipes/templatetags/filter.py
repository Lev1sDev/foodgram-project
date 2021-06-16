from django import template

register = template.Library()


@register.filter
def exists(value, field):
    return value.filter(user=field)
