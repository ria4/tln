import string

from django import template


register = template.Library()


@register.filter
def truncatedesc(arg1, arg2):
    """
    Truncate some oeuvre comment for tw/og cards.
    Keep first arg2-th characters, then remove the bits of the last word and add ellipsis.
    """
    if len(arg1) < arg2:
        return arg1

    res = arg1[:arg2]
    res = res[:res.rfind(" ")]
    while res[-1] in string.punctuation:
        res = res[:-1]
    return res + "..."
