from django import template

register = template.Library()

@register.filter
def percentage(part, whole):
    try:
        return round(100 * float(part) / float(whole), 2)
    except (ValueError, ZeroDivisionError):
        return 0
