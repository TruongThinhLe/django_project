from django import template
from datetime import datetime

register=template.Library()

@register.simple_tag
def dead_plan(date_end,date_start):
    return int((date_end-date_start).days)
@register.simple_tag
def rate_plan(date_end,date_start):
    now=datetime.date(datetime.now())
    return int(((now-date_start).days)/((date_end-date_start).days)*100)