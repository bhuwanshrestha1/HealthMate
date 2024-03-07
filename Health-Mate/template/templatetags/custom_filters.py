# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='format_date')
def format_date(value, arg='%A, %d %B %Y'):
    return value.strftime(arg)

@register.filter(name='day_of_week_order')
def day_of_week_order(day_name):
    days_in_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return days_in_week.index(day_name) + 1