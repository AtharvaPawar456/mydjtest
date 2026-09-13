from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def price(value):
    """
    Formats a numeric-looking price string with thousands separators
    (e.g. "15000" -> "15,000"). Passes through unchanged anything that
    isn't a plain number, such as the "*" placeholder these TextFields
    default to.
    """
    if value is None:
        return value
    text = str(value).strip()
    if not text or text == '*':
        return value
    try:
        number = float(text.replace(',', ''))
    except ValueError:
        return value
    if number == int(number):
        return intcomma(int(number))
    return intcomma(number)
