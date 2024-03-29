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
        href = reverse('detail_oeuvre', kwargs={'slug': film.slug})
        return format_html("<a href=%s>%s</a>" % (href, film.title_vf))


def cinemalink_with_len(cinema, cinema_unsure=False, cinema_name_override=None):
    "Return a link to the Cinema, in long form."""
    prefix = None
    a_text = cinema_name_override or cinema.name_long
    for prefix_possible in CINEMA_LONGNAME_PREFIXES:
        if a_text.startswith(prefix_possible):
            prefix = prefix_possible
            a_text = a_text[len(prefix):]
            break
    href = reverse('detail_cinema', kwargs={'slug': cinema.slug})
    res = "%s<a href=%s>%s</a>" % (prefix, href, a_text)
    l = len(prefix + a_text)
    if cinema_unsure:
        maybe = " (peut-être)"
        res += maybe
        l += len(maybe)
    return format_html(res), l

@register.filter
def cinemalink(cinema, cinema_unsure=False):
    cl, l = cinemalink_with_len(cinema, cinema_unsure=False)
    return cl


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

    "commencé en juin 2022",

    "vu le 16 juin 2022 au <a href=...>Katorza</a>"

    "         vu le 12 novembre 2019
    au <a...>Max Linder Panorama</a>"

    "   vu le 3 mars 2017,
           le 12 mai 2019
    et le 27 octobre 2022"
    """
    mtype_prefix, mtype_accord = MTYPE_SPAN_MAP.get(mtype)
    res = ""
    n = len(spans)
    for i, span in enumerate(spans):
        if i == 0:
            if not span.ongoing:
                res += mtype_prefix
            else:
                accord = "e" if mtype_accord else ""
                res += f"commencé{accord} "
        else:
            if span.ongoing:
                res += "depuis "
        if span.ongoing:
            res += fancydate(
                span,
                date_attrname='date_start',
                le=True,
                en=(i==0),
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
                if span.seance.cinema:
                    cl, len_cl_stripped = cinemalink_with_len(
                        span.seance.cinema,
                        span.seance.cinema_unsure,
                        span.seance.cinema_name_long_override,
                    )
                    len_date = len(res)
                    if span.date_start.day == 1:
                        # strip 1<sup>er</sup>
                        len_date -= 12
                    adjust = -2 if n == 1 else 8
                    if (
                        len_cl_stripped > len_date + adjust
                        and len_date + len_cl_stripped > 38
                    ):
                        res += "<br>"
                    else:
                        res += " "
                    res += cl
                else:
                    res += ", dans un cinéma oublié"
        elif (
            span.date_start.month == span.date_end.month
            and span.date_start.year == span.date_end.year
            and (span.date_start_du or span.date_end_du)
        ):
            res += fancydate(
                span,
                date_attrname='date_start',
                le=True,
                en=True,
                mois=True,
                annee=True,
            )
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
