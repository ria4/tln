from datetime import datetime

from django import template

from tagging.models import Tag
from tagging.utils import calculate_cloud

from zinnia.models.entry import Entry


register = template.Library()


@register.simple_tag
def get_articles_on_day(date):
    """
    Do not use this on dates when no article was published!
    """
    entries = Entry.objects.filter(publication_date__year=date.year,
                                   publication_date__month=date.month,
                                   publication_date__day=date.day)
    articles = [{'title': entry.title, 'url': '/blog/%s' % entry.slug}
                 for entry in entries]
    return articles

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
