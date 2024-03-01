"""EntryAdmin for Zinnia"""
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models import Q
from django.forms import ModelForm
from django.urls import NoReverseMatch
from django.urls import reverse
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.html import format_html
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from blog import settings
from blog.admin.filters import AuthorListFilter
from blog.admin.filters import CategoryListFilter
from blog.admin.forms import EntryAdminForm
from blog.comparison import EntryPublishedVectorBuilder
from blog.managers import HIDDEN
from blog.managers import PUBLISHED
from blog.models.author import Author


class FilterOutSuperuserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allowed_users'].queryset = User.objects.filter(is_superuser=False)


class EntryAdmin(admin.ModelAdmin):
    """
    Admin for Entry model.
    """
    form = EntryAdminForm
    date_hierarchy = 'publication_date'
    fieldsets = (
        (_('Content'), {
            'fields': (
                ('title', 'status'),
                'lang',
                'content',
                'publication_date',
            )}),
        ('Liens', {'fields': ('tags', 'slug')}),
        (_('Privacy'), {
            'fields': ('login_required', 'allowed_users'),
            'classes': ('collapse', 'collapse-closed')}),
        ('Technique', {
            'fields': ('sites', 'authors'),
            'classes': ('collapse', 'collapse-closed')}),
    )
    form = FilterOutSuperuserForm
    list_filter = ('publication_date', 'status')
    list_display = ('get_title', 'get_tags', 'get_is_visible',
                    'get_short_url', 'publication_date')
    sortable_by = ('publication_date')
    radio_fields = {'content_template': admin.VERTICAL,
                    'detail_template': admin.VERTICAL}
    filter_horizontal = ('allowed_users',)
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'excerpt', 'content', 'tags')
    actions = ['make_mine', 'make_published', 'make_hidden',
               'close_comments', 'close_pingbacks', 'close_trackbacks',
               'ping_directories', 'put_on_top',
               'mark_featured', 'unmark_featured']
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(EntryAdmin, self).__init__(model, admin_site)

    # Custom Display
    def get_title(self, entry):
        """
        Return the title with word count and number of comments.
        """
        title = _('%(title)s (%(word_count)i words)') % \
            {'title': entry.title, 'word_count': entry.word_count}
        reaction_count = int(entry.comment_count +
                             entry.pingback_count +
                             entry.trackback_count)
        if reaction_count:
            return ngettext_lazy(
                '%(title)s (%(reactions)i reaction)',
                '%(title)s (%(reactions)i reactions)', reaction_count) % \
                {'title': title,
                 'reactions': reaction_count}
        return title
    get_title.short_description = _('title')

    def get_authors(self, entry):
        """
        Return the authors in HTML.
        """
        try:
            return format_html_join(
                ', ', '<a href="{}" target="blank">{}</a>',
                [(author.get_absolute_url(),
                  getattr(author, author.USERNAME_FIELD))
                 for author in entry.authors.all()])
        except NoReverseMatch:
            return ', '.join(
                [conditional_escape(getattr(author, author.USERNAME_FIELD))
                 for author in entry.authors.all()])
    get_authors.short_description = _('author(s)')

    def get_categories(self, entry):
        """
        Return the categories linked in HTML.
        """
        try:
            return format_html_join(
                ', ', '<a href="{}" target="blank">{}</a>',
                [(category.get_absolute_url(), category.title)
                 for category in entry.categories.all()])
        except NoReverseMatch:
            return ', '.join([conditional_escape(category.title)
                              for category in entry.categories.all()])
    get_categories.short_description = _('category(s)')

    def get_tags(self, entry):
        """
        Return the tags linked in HTML.
        """
        try:
            return format_html_join(
                ', ', '<a href="{}" target="blank">{}</a>',
                [(reverse('blog:tag_detail', args=[tag]), tag)
                 for tag in entry.tags_list])
        except NoReverseMatch:
            return conditional_escape(entry.tags)
    get_tags.short_description = _('tag(s)')

    def get_sites(self, entry):
        """
        Return the sites linked in HTML.
        """
        try:
            index_url = reverse('blog:entry_archive_index')
        except NoReverseMatch:
            index_url = ''
        return format_html_join(
            ', ', '<a href="{}://{}{}" target="blank">{}</a>',
            [(settings.PROTOCOL, site.domain, index_url,
              conditional_escape(site.name)) for site in entry.sites.all()])
    get_sites.short_description = _('site(s)')

    def get_short_url(self, entry):
        """
        Return the short url in HTML.
        """
        try:
            short_url = entry.short_url
        except NoReverseMatch:
            short_url = entry.get_absolute_url()
        return format_html('<a href="{url}" target="blank">{url}</a>',
                           url=short_url)
    get_short_url.short_description = _('short url')

    def get_is_visible(self, entry):
        """
        Admin wrapper for entry.is_visible.
        """
        return entry.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    # Custom Methods
    def get_queryset(self, request):
        """
        Make special filtering by user's permissions.
        """
        if not request.user.has_perm('blog.can_view_all'):
            queryset = self.model.objects.filter(authors__pk=request.user.pk)
        else:
            queryset = super(EntryAdmin, self).get_queryset(request)
        return queryset.prefetch_related('categories', 'authors', 'sites')

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating an entry.
        """
        get_data = super(EntryAdmin, self).get_changeform_initial_data(request)
        return get_data or {
            'sites': [Site.objects.get_current().pk],
            'authors': [request.user.pk]
        }

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filter the disposable authors.
        """
        if db_field.name == 'authors':
            kwargs['queryset'] = Author.objects.filter(
                Q(is_staff=True) | Q(entries__isnull=False)
                ).distinct()

        return super(EntryAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """
        Return readonly fields by user's permissions.
        """
        readonly_fields = list(super(EntryAdmin, self).get_readonly_fields(
            request, obj))

        if not request.user.has_perm('blog.can_change_status'):
            readonly_fields.append('status')

        if not request.user.has_perm('blog.can_change_author'):
            readonly_fields.append('authors')

        return readonly_fields

    def get_actions(self, request):
        """
        Define actions by user's permissions.
        """
        actions = super(EntryAdmin, self).get_actions(request)
        if not actions:
            return actions
        if (not request.user.has_perm('blog.can_change_author') or
                not request.user.has_perm('blog.can_view_all')):
            del actions['make_mine']
        if not request.user.has_perm('blog.can_change_status'):
            del actions['make_hidden']
            del actions['make_published']
        if not settings.PING_DIRECTORIES:
            del actions['ping_directories']

        return actions

    # Custom Actions
    def make_mine(self, request, queryset):
        """
        Set the entries to the current user.
        """
        author = Author.objects.get(pk=request.user.pk)
        for entry in queryset:
            if author not in entry.authors.all():
                entry.authors.add(author)
        self.message_user(
            request, _('The selected entries now belong to you.'))
    make_mine.short_description = _('Set the entries to the user')

    def make_published(self, request, queryset):
        """
        Set entries selected as published.
        """
        queryset.update(status=PUBLISHED)
        EntryPublishedVectorBuilder().cache_flush()
        self.ping_directories(request, queryset, messages=False)
        self.message_user(
            request, _('The selected entries are now marked as published.'))
    make_published.short_description = _('Set entries selected as published')

    def make_hidden(self, request, queryset):
        """
        Set entries selected as hidden.
        """
        queryset.update(status=HIDDEN)
        EntryPublishedVectorBuilder().cache_flush()
        self.message_user(
            request, _('The selected entries are now marked as hidden.'))
    make_hidden.short_description = _('Set entries selected as hidden')

    def close_comments(self, request, queryset):
        """
        Close the comments for selected entries.
        """
        queryset.update(comment_enabled=False)
        self.message_user(
            request, _('Comments are now closed for selected entries.'))
    close_comments.short_description = _('Close the comments for '
                                         'selected entries')

    def close_pingbacks(self, request, queryset):
        """
        Close the pingbacks for selected entries.
        """
        queryset.update(pingback_enabled=False)
        self.message_user(
            request, _('Pingbacks are now closed for selected entries.'))
    close_pingbacks.short_description = _(
        'Close the pingbacks for selected entries')

    def close_trackbacks(self, request, queryset):
        """
        Close the trackbacks for selected entries.
        """
        queryset.update(trackback_enabled=False)
        self.message_user(
            request, _('Trackbacks are now closed for selected entries.'))
    close_trackbacks.short_description = _(
        'Close the trackbacks for selected entries')

    def put_on_top(self, request, queryset):
        """
        Put the selected entries on top at the current date.
        """
        queryset.update(publication_date=timezone.now())
        self.ping_directories(request, queryset, messages=False)
        self.message_user(request, _(
            'The selected entries are now set at the current date.'))
    put_on_top.short_description = _(
        'Put the selected entries on top at the current date')

    def mark_featured(self, request, queryset):
        """
        Mark selected as featured post.
        """
        queryset.update(featured=True)
        self.message_user(
            request, _('Selected entries are now marked as featured.'))
    mark_featured.short_description = _('Mark selected entries as featured')

    def unmark_featured(self, request, queryset):
        """
        Un-Mark selected featured posts.
        """
        queryset.update(featured=False)
        self.message_user(
            request, _('Selected entries are no longer marked as featured.'))
    unmark_featured.short_description = _(
        'Unmark selected entries as featured')
