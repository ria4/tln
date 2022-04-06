from django import template
from django.urls import reverse
from django.utils.html import format_html

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
    if seance.film:
        title_vf = seance.film.info.titles.vf
        href = reverse('detail_oeuvre', kwargs={'slug': seance.film.slug})
        return format_html("<a href=%s>%s</a>" % (href, title_vf))
    else:
        return seance.seance_title
