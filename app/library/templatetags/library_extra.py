import datetime
from django import template

register = template.Library()


@register.simple_tag
def has_access(user, category):
    return user.has_access(category)