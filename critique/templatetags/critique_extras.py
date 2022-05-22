from django import template
from django.urls import reverse
from django.utils.html import format_html

from tln.templatetags.tln_extras import fancydate

from critique.constants import CINEMA_LONGNAME_PREFIXES, MTYPE_SPAN_MAP

register = template.Library()


@register.filter
def seancecinemashort(seance):
    """Return a pretty cinema name for a Seance.

    Examples : "La Filmo", "MK2 Hautefeuille ?", "?".
    """

    cinema = ""

    if seance.cinema_name_short_override:
        cinema = seance.cinema_name_short_override
    elif seance.cinema and seance.cinema.name_short:
        cinema = seance.cinema.name_short
    elif seance.cinema:
        cinema = seance.cinema.name

    if seance.cinema_unsure:
        if cinema:
            cinema += " "
        cinema += "?"

    return cinema


@register.filter
def seancefilmlink(seance):
    """Return either a link to the Oeuvre, or the seance title."""
    if seance.seance_title:
        return seance.seance_title
    else:
        film = seance.oeuvre_span.oeuvre
        title_vf = film.info.titles.vf
        href = reverse('detail_oeuvre', kwargs={'slug': film.slug})
        return format_html("<a href=%s>%s</a>" % (href, title_vf))


@register.filter
def cinemalink(cinema):
    "Return a link to the Cinema, in long form."""
    prefix = None
    a_text = cinema.name_long
    for prefix_possible in CINEMA_LONGNAME_PREFIXES:
        if cinema.name_long.startswith(prefix_possible):
            prefix = prefix_possible
            a_text = cinema.name_long[len(prefix):]
            break
    href = reverse('detail_cinema', kwargs={'slug': cinema.slug})
    return format_html(" %s<a href=%s>%s</a>" % (prefix, href, a_text))
    #return format_html(f" {prefix}<a href={href}>{a_text}</a>")


@register.filter
def ellipsiscolor(seance):
    """Return a class for setting the right color of overflow ellipsis."""
    return 'ellipsis-black' if seance.seance_title else ''


@register.simple_tag
def fancyspans(mtype, spans):
    """Return a pretty list of dates for a queryset of OeuvreSpan.

    Examples:

    "vu le 15 mai 2022"

    "lu entre mai et octobre 2022",

    "jeu en cours depuis juin 2022",

    "vu le 16 juin 2022 au <a href=...>Katorza</a>"

    "   vu le 3 mars 2017,
           le 12 mai 2019
    et le 27 octobre 2022"
    """
    mtype_prefix, mtype_prefix_ongoing = MTYPE_SPAN_MAP.get(mtype)
    res = ""
    n = len(spans)
    for i, span in enumerate(spans):
        if i == 0:
            if not span.ongoing:
                res += mtype_prefix
            else:
                res += mtype_prefix_ongoing + "en cours depuis "
        else:
            if span.ongoing:
                res += "depuis "
        if span.ongoing:
            res += fancydate(
                span,
                date_attrname='date_start',
                le=True,
                en=False,
                mois=True,
                annee=True,
            )
        elif span.date_start == span.date_end:
            res += fancydate(
                span,
                date_attrname='date_start',
                le=True,
                en=True,
                mois=True,
                annee=True,
            )
            if hasattr(span, 'seance'):
                res += cinemalink(span.seance.cinema)
        else:
            mois = True
            annee = span.date_start.year != span.date_end.year
            if not annee:
                mois = span.date_start.month != span.date_end.month
            start = fancydate(
                span,
                date_attrname='date_start',
                le=True,
                en=False,
                mois=mois,
                annee=annee,
            )
            end = fancydate(
                span,
                date_attrname='date_end',
                le=True,
                en=False,
                mois=True,
                annee=True,
            )
            res += "entre %s et %s" % (start, end)
        if i < n - 1:
            res += ",<br>"
        if i == n - 2:
            res += "et "
    return format_html(res)
