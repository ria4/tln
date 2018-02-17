from datetime import datetime

from django import template

from tagging.models import Tag
from tagging.utils import calculate_cloud

from zinnia.models.entry import Entry


register = template.Library()


@register.simple_tag
def get_entries_on_year_length(date, is_superuser=False):
    # Do not use this on dates when no entry was published!
    if is_superuser is True:
        queryset = Entry.objects
    else:
        queryset = Entry.published
    entries = queryset.filter(publication_date__year=date.year)
    return len(entries)

@register.simple_tag
def get_entries_on_month_length(date, is_superuser=False):
    # Do not use this on dates when no entry was published!
    if is_superuser is True:
        queryset = Entry.objects
    else:
        queryset = Entry.published
    entries = queryset.filter(publication_date__year=date.year,
                              publication_date__month=date.month)
    return len(entries)

@register.simple_tag
def get_entries_on_day(date, is_superuser=False):
    # Do not use this on dates when no entry was published!
    if is_superuser is True:
        queryset = Entry.objects
    else:
        queryset = Entry.published
    entries = queryset.filter(publication_date__year=date.year,
                              publication_date__month=date.month,
                              publication_date__day=date.day)
    entries_clean = [{'title': entry.title, 'url': '/blog/%s' % entry.slug}
                     for entry in entries]
    return entries_clean


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_archives_entries_tree_su_sensitive(context,
        template='zinnia/tags/entries_archives_tree.html'):
    if context['request'].user.is_superuser:
        queryset = Entry.objects
    else:
        queryset = Entry.published
    return {'template': template,
            'archives': queryset.datetimes(
                'publication_date', 'day', order='ASC'),
            'is_superuser': context['request'].user.is_superuser}


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
