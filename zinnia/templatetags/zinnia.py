"""Template tags and filters for Zinnia"""
from datetime import datetime
from hashlib import md5
import re
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from django_comments import get_model as get_comment_model
from django_comments.models import CommentFlag

from tagging.models import Tag
from tagging.utils import calculate_cloud

from ..managers import DRAFT
from ..managers import tags_published
from ..models.author import Author
from ..models.category import Category
from ..models.entry import Entry
from ..settings import PINGBACK, PROTOCOL, TRACKBACK


WIDONT_REGEXP = re.compile(
    r'\s+(\S+\s*)$')
DOUBLE_SPACE_PUNCTUATION_WIDONT_REGEXP = re.compile(
    r'\s+([-+*/%=;:!?]+&nbsp;\S+\s*)$')
END_PUNCTUATION_WIDONT_REGEXP = re.compile(
    r'\s+([?!]+\s*)$')

register = Library()


@register.inclusion_tag('zinnia/tags/dummy.html')
def get_draft_entries(number=5,
                      template='zinnia/tags/entries_draft.html'):
    """
    Return the last draft entries.
    """
    return {'template': template,
            'entries': Entry.objects.filter(status=DRAFT)[:number]}


@register.inclusion_tag('zinnia/tags/dummy.html')
def get_recent_comments(number=5, template='zinnia/tags/comments_recent.html'):
    """
    Return the most recent comments.
    """
    # Using map(smart_str... fix bug related to issue #8554
    entry_published_pks = map(smart_str,
                              Entry.published.values_list('id', flat=True))
    content_type = ContentType.objects.get_for_model(Entry)

    comments = get_comment_model().objects.filter(
        Q(flags=None) | Q(flags__flag=CommentFlag.MODERATOR_APPROVAL),
        content_type=content_type, object_pk__in=entry_published_pks,
        is_public=True).order_by('-pk')[:number]

    comments = comments.prefetch_related('content_object')

    return {'template': template,
            'comments': comments}


@register.simple_tag
def get_gravatar(email, size=80, rating='g', default=None,
                 protocol=PROTOCOL):
    """
    Return url for a Gravatar.
    """
    gravatar_protocols = {'http': 'http://www',
                          'https': 'https://secure'}
    url = '%s.gravatar.com/avatar/%s' % (
        gravatar_protocols[protocol],
        md5(email.strip().lower().encode('utf-8')).hexdigest())
    options = {'s': size, 'r': rating}
    if default:
        options['d'] = default

    url = '%s?%s' % (url, urlencode(options))
    return url.replace('&', '&amp;')


@register.simple_tag
def get_tags():
    """
    Return the published tags.
    """
    return Tag.objects.usage_for_queryset(
        Entry.published.all())


@register.filter(needs_autoescape=True)
@stringfilter
def widont(value, autoescape=None):
    """
    Add an HTML non-breaking space between the final
    two words of the string to avoid "widowed" words.
    """
    esc = autoescape and conditional_escape or (lambda x: x)

    def replace(matchobj):
        return '&nbsp;%s' % matchobj.group(1)

    value = END_PUNCTUATION_WIDONT_REGEXP.sub(replace, esc(smart_str(value)))
    value = WIDONT_REGEXP.sub(replace, value)
    value = DOUBLE_SPACE_PUNCTUATION_WIDONT_REGEXP.sub(replace, value)

    return mark_safe(value)


@register.filter
def comment_admin_urlname(action):
    """
    Return the admin URLs for the comment app used.
    """
    comment = get_comment_model()
    return 'admin:%s_%s_%s' % (
        comment._meta.app_label, comment._meta.model_name,
        action)


@register.filter
def user_admin_urlname(action):
    """
    Return the admin URLs for the user app used.
    """
    user = get_user_model()
    return 'admin:%s_%s_%s' % (
        user._meta.app_label, user._meta.model_name,
        action)


@register.inclusion_tag('zinnia/tags/dummy.html')
def zinnia_statistics(template='zinnia/tags/statistics.html'):
    """
    Return statistics on the content of Zinnia.
    """
    content_type = ContentType.objects.get_for_model(Entry)
    discussions = get_comment_model().objects.filter(
        content_type=content_type)

    entries = Entry.published
    categories = Category.objects
    tags = tags_published()
    authors = Author.published
    replies = discussions.filter(
        flags=None, is_public=True)
    pingbacks = discussions.filter(
        flags__flag=PINGBACK, is_public=True)
    trackbacks = discussions.filter(
        flags__flag=TRACKBACK, is_public=True)
    rejects = discussions.filter(is_public=False)

    entries_count = entries.count()
    replies_count = replies.count()
    pingbacks_count = pingbacks.count()
    trackbacks_count = trackbacks.count()

    if entries_count:
        first_entry = entries.order_by('publication_date')[0]
        last_entry = entries.latest()
        months_count = (last_entry.publication_date -
                        first_entry.publication_date).days / 31.0
        entries_per_month = entries_count / (months_count or 1.0)

        comments_per_entry = float(replies_count) / entries_count
        linkbacks_per_entry = float(pingbacks_count + trackbacks_count) / \
            entries_count

        total_words_entry = 0
        for e in entries.all():
            total_words_entry += e.word_count
        words_per_entry = float(total_words_entry) / entries_count

        words_per_comment = 0.0
        if replies_count:
            total_words_comment = 0
            for c in replies.all():
                total_words_comment += len(c.comment.split())
            words_per_comment = float(total_words_comment) / replies_count
    else:
        words_per_entry = words_per_comment = entries_per_month = \
            comments_per_entry = linkbacks_per_entry = 0.0

    return {'template': template,
            'entries': entries_count,
            'categories': categories.count(),
            'tags': tags.count(),
            'authors': authors.count(),
            'comments': replies_count,
            'pingbacks': pingbacks_count,
            'trackbacks': trackbacks_count,
            'rejects': rejects.count(),
            'words_per_entry': words_per_entry,
            'words_per_comment': words_per_comment,
            'entries_per_month': entries_per_month,
            'comments_per_entry': comments_per_entry,
            'linkbacks_per_entry': linkbacks_per_entry}


@register.simple_tag
def get_entries_on_day(date, is_superuser=False, user_id=0):
    # Do not use this on dates when no entry was published!
    queryset = Entry.objects.filter(status=2, login_required=False)
    if is_superuser is True:
        queryset = Entry.objects
    elif user_id:
        queryset |= Entry.objects.filter(allowed_users__exact=user_id)
    entries = queryset.filter(publication_date__year=date.year,
                              publication_date__month=date.month,
                              publication_date__day=date.day)
    entries_clean = [{'title': entry.title, 'url': '/blog/%s' % entry.slug, 'lang': entry.lang}
                     for entry in entries]
    return entries_clean


@register.simple_tag
def tag_entries_with_year(entries):
    return [{'entry': entry, 'year': entry.publication_date.strftime('%Y')} for entry in entries]


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_archives_entries_tree_su_sensitive(context,
        template='zinnia/tags/entries_archives_tree.html'):
    user = context['request'].user
    user_id = 0
    queryset = Entry.objects.filter(status=2,
                                    login_required=False)
    if user.is_superuser:
        queryset = Entry.objects
    elif user.is_authenticated:
        User = get_user_model()
        user_id = User.objects.get(username=user.username).id
        queryset |= Entry.objects.filter(allowed_users__exact=user_id)
    publication_date = None
    if 'object' in context:
        publication_date = context['object'].publication_date
    return {'template': template,
            'archives': queryset.datetimes('publication_date', 'day', order='ASC'),
            'publication_date': publication_date,
            'is_superuser': user.is_superuser,
            'user_id': user_id}


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_tag_cloud_su_sensitive(context, steps=6, min_count=None,
                               template='zinnia/tags/tag_cloud.html'):
    if context['request'].user.is_superuser:
        queryset = Entry.objects.all()
    else:
        queryset = Entry.published.all()
    tags = Tag.objects.usage_for_queryset(queryset, counts=True, min_count=min_count)
    return {'template': template,
            'tags': calculate_cloud(tags, steps),
            'context_tag': context.get('tag')}
