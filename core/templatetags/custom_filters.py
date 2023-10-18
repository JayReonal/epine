from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils.timezone import make_aware

register = template.Library()

@register.filter(name='format_number')
def format_number(value):
    if value is None:
        return "0"
    return "{:,.2f}".format(value)

@register.filter
def hours_ago(value):
    now = make_aware(datetime.now())
    diff = now - value

    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    if diff.days == 0:
        if hours > 0:
            if hours == 1:
                hours_str = f"{hours} hour"
            else:
                hours_str = f"{hours} hours"

            if minutes > 0:
                if minutes == 1:
                    minutes_str = f"{minutes} minute"
                else:
                    minutes_str = f"{minutes} minutes"

                return f"{hours_str} and {minutes_str} ago"
            else:
                return f"{hours_str} ago"
        elif minutes > 0:
            if minutes == 1:
                minutes_str = f"{minutes} minute"
            else:
                minutes_str = f"{minutes} minutes"

            return f"{minutes_str} ago"
        else:
            return "just now"
    else:
        return value.strftime("%b %d, %Y %I:%M %p")