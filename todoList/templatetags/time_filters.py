from django import template
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def to_moscow_time(value):
    return localtime(value)