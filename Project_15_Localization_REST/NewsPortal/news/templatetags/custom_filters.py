from django import template

register = template.Library()

post_type = {
    "N": "News",
    "A": "Article"
}


@register.filter()
def get_post_type(value):
    return post_type[value]


@register.filter()
def change_date_view(value, format_str="%Y-%m-%d %H:%M:%:S"):
    return f"{value.strftime(format_str)}"


@register.filter()
def censor(value):
    ban_words =[
    "text"
]
    for word in ban_words:
        value = value.replace(word, word[0] + "*" * (len(word) - 1))

    return value