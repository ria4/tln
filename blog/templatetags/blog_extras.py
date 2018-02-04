
from datetime import datetime
from django import template
from zinnia.models.entry import Entry

register = template.Library()

@register.simple_tag
def get_article_on_day(date):
    """
    Do not use this on dates when no article was published!
    """
    entry = Entry.objects.filter(publication_date__year=date.year,
                                 publication_date__month=date.month,
                                 publication_date__day=date.day)[0]
    url = '/blog/%.4d/%.2d/%.2d/%s' % (date.year, date.month, date.day, entry.slug)
    return {'title': entry.title, 'url': url}

