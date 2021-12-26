from datetime import timedelta

import markdown
from django import template

register = template.Library()


@register.filter
def duration(td: timedelta):
    total_millis = int(td / timedelta(milliseconds=1))

    minutes = total_millis // 60000
    seconds = (total_millis % 60000) // 1000
    millis = total_millis % 1000

    return f"{minutes}:{seconds:02d}:{millis:03d}"

@register.simple_tag
def alias(obj):
    """
    Alias Tag
    """
    return obj

@register.simple_tag
def tires(tire_string):
    """
    Returns list of images (static)
    """
    
    tires = []
    if tire_string:
        for tire in tire_string:
            match tire:
                case "S":
                    tires.append('leaderboard/tires/soft.png')
                case "M":
                    tires.append('leaderboard/tires/medium.png') 
                case "H":
                    tires.append('leaderboard/tires/hard.png') 
                case "W":
                    tires.append('leaderboard/tires/wet.png') 
                case "I":
                    tires.append('leaderboard/tires/inter.png') 
    return tires

@register.filter
def parse_markdown(text):
    md = markdown.Markdown()
    html = md.convert(text)
    return html
