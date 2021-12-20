from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def duration(td: timedelta):
    total_millis = int(td / timedelta(milliseconds=1))

    minutes = total_millis // 60000
    seconds = (total_millis % 60000) // 1000
    millis = total_millis % 1000

    return f"{minutes}:{seconds:02d}:{millis:03d}"
