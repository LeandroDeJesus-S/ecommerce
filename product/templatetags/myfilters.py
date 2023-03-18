from django.template import Library
from utils import functions

register = Library()


@register.filter
def format_money(value):
    return functions.format_money_value(value)


@register.filter
def get_cart_quantity(value):
    return functions.get_cart_quantity(value)

@register.filter
def total_cart(value):
    return functions.amount(value)


@register.filter
def calculate_age(value):
    return functions.calculate_age(value)

