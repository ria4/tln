import string

from django import template
from django.utils.dateformat import format as date_format
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime

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


@register.simple_tag
def fancydate(obj, date_attrname='date', en=False, le=False, mois=True, annee=False):
    """Return a pretty date, e.g. for a Seance or a Commentaire.

    Django would handle localization in one of its templates,
    but here it has to be done manually."""

    dt = localtime(getattr(obj, date_attrname))
    res = ""

    if getattr(obj, f'{date_attrname}_mu', None):
        if en:
            res += "en "
        res += f"{date_format(dt, 'Y')}"
        return res

    if getattr(obj, f'{date_attrname}_du', None):
        if en:
            res += "en "
        res += f"{date_format(dt, 'F')}"
        if annee:
            res += f"{date_format(dt, ' Y')}"
        return res

    if le:
        res += "le "
    res += date_format(dt, 'j')
    if dt.day == 1:
        res += "<sup>er</sup>"
    if mois:
        res += f" {date_format(dt, 'F')}"
    if annee:
        res += f" {date_format(dt, 'Y')}"

    return mark_safe(res)


@register.filter
def get_item(mydict, key):
    return mydict.get(key)
