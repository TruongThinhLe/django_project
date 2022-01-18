from django import template
from datetime import datetime
from polls.algorithm import rate

register=template.Library()

@register.simple_tag
def dead_plan(date_end,date_start):
    return int((date_end-date_start).days)
@register.simple_tag
def rate_plan(date_end,date_start):
    result=rate(date_end=date_end,date_start=date_start)
    return result