from django import template
from django.utils.dateformat import format as date_format
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime

register = template.Library()


@register.filter()
def critiquedate(obj, opts=''):
    """Return a pretty date for a Seance or a Commentaire.

    Django would handle localization in one of its templates,
    but here it has to be done manually."""

    opts = opts.split(',')
    dt = localtime(obj.date)
    res = ""

    if getattr(obj, 'date_month_unknown', None):
        if 'no_en' not in opts:
            res += "en "
        res += f"{date_format(dt, 'Y')}"
        return res

    if getattr(obj, 'date_day_unknown', None):
        if 'no_en' not in opts:
            res += "en "
        res += f"{date_format(dt, 'F Y')}"
        return res

    if 'no_le' not in opts:
        res += "le "
    res += date_format(dt, 'j')
    if dt.day == 1:
        res += "<sup>er</sup>"
    res += f" {date_format(dt, 'F')}"
    if 'no_year' not in opts:
        res += f" {date_format(dt, 'Y')}"

    return mark_safe(res)
