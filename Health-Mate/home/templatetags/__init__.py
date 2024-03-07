# __init__.py
from django import template
from .custom_filters import format_date

register = template.Library()
register.filter('format_date', format_date)