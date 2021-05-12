from datetime import datetime

from django import template

from tagging.models import Tag
from tagging.utils import calculate_cloud

from zinnia.models.entry import Entry

from blog.models import EntryCustom


register = template.Library()


@register.simple_tag
def get_entries_on_day(date, is_superuser=False):
    # Do not use this on dates when no entry was published!
    if is_superuser is True:
        queryset = EntryCustom.objects
    else:
        queryset = EntryCustom.objects.filter(entry__status=2,
                                              entry__login_required=False)
    entries = queryset.filter(entry__publication_date__year=date.year,
                              entry__publication_date__month=date.month,
                              entry__publication_date__day=date.day)
    entries_clean = [{'title': entryc.entry.title, 'url': '/blog/%s' % entryc.entry.slug, 'lang': entryc.lang}
                     for entryc in entries]
    return entries_clean


@register.simple_tag
def tag_entries_with_year(entries):
    return [{'entry': entry, 'year': entry.publication_date.strftime('%Y')} for entry in entries]


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_archives_entries_tree_su_sensitive(context,
        template='zinnia/tags/entries_archives_tree.html'):
    queryset = EntryCustom.objects.filter(entry__status=2,
                                          entry__login_required=False)
    if context['request'].user.is_superuser:
        queryset = EntryCustom.objects
    publication_date = None
    if 'object' in context:
        publication_date = context['object'].publication_date
    return {'template': template,
            'archives': queryset.datetimes(
                'entry__publication_date', 'day', order='ASC'),
            'publication_date': publication_date,
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
