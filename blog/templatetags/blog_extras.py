from datetime import datetime

from django import template

from tagging.models import Tag
from tagging.utils import calculate_cloud

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

@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_tag_cloud_su_sensitive(context, steps=6, min_count=None,
                               template='zinnia/tags/tag_cloud.html'):
    if context['request'].user.is_superuser:
        queryset = Entry.objects.all()
    else:
        queryset = Entry.published.all()
    tags = Tag.objects.usage_for_queryset(
        queryset, counts=True,
        min_count=min_count)
    return {'template': template,
            'tags': calculate_cloud(tags, steps),
            'context_tag': context.get('tag')}
