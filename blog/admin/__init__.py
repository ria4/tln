"""Admin of Zinnia"""
from django.contrib import admin

from blog.admin.category import CategoryAdmin
from blog.admin.entry import EntryAdmin
from blog.models.category import Category
from blog.models.entry import Entry
from blog.settings import ENTRY_BASE_MODEL


if ENTRY_BASE_MODEL == 'blog.models_bases.entry.AbstractEntry':
    admin.site.register(Entry, EntryAdmin)

admin.site.register(Category, CategoryAdmin)
