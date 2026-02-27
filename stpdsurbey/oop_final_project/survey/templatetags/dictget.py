from django import template

register = template.Library()

@register.filter(name='dictget')
def dictget(dict_data, key):
    return dict_data.get(key)