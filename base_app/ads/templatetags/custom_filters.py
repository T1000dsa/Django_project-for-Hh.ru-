from django import template

register = template.Library()

@register.filter
def get_exchange(obj, user_pk):
    return obj.get_exchange(user_pk)