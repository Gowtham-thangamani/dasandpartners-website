from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    """Multiply the value by the arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='subtract')
def subtract(value, arg):
    """Subtract the arg from the value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='divide')
def divide(value, arg):
    """Divide the value by the arg"""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return ''


