from django.template import Library
from utils import functions

register = Library()


@register.filter
def format_money(value):
    return functions.format_money_value(value)


@register.filter
def get_quantity(value):
    return functions.get_total(value)
