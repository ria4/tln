"""Models for Zinnia"""
from blog.models.author import Author
from blog.models.category import Category
from blog.models.entry import Entry

# Here we import the Zinnia's Model classes
# to register the Models at the loading, not
# when the Zinnia's URLs are parsed. Issue #161.
# Issue #161, seems not valid since Django 1.7.
__all__ = [Entry.__name__,
           Author.__name__,
           Category.__name__]
