from django import template


register = template.Library()


@register.filter
def stripgallery(title):
    """
    Remove gallery prefix from photo titles of the form gallery__mytitle.
    """
    idx = title.find("__")
    if idx < 0:
        return title
    return title[idx+2:]
