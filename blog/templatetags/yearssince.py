from django.utils.timesince import timesince
from django import template
import mistune

register = template.Library()

@register.filter
def yearssince(value):
    years_months = timesince(value)
    return years_months.split(',')[0]
