from django import template

register = template.Library()


@register.simple_tag
def format_date(date, format_string):
    return date.strftime(format_string)
