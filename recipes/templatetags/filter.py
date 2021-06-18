from django import template

register = template.Library()


@register.filter
def exists(value, field):
    return value.filter(user=field)


@register.filter
def tag_filter(value, field):
    url = '?'
    if field not in value:
        if len(value) == 0:
            url += f'tag={field.slug}'
        else:
            url += f'tag={field.slug}&'
    for i in range(len(value)):
        if value[i] == field:
            continue
        if i + 1 == len(value):
            url += f'tag={value[i].slug}'
        else:
            url += f'tag={value[i].slug}&'
    return url
