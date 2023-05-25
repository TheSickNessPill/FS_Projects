import datetime

from django import template

register = template.Library()

@register.filter
def lower_custom(value):
    return value.lower()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.filter
def hide_forbidden(value):
    forbidden_words = ["asd", "qwe", "xzc"]
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)