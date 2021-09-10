from django import template

from photos.models import GalleryCustom


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

@register.inclusion_tag('photologue/tags/galleries.html')
def get_public_photo_galleries():
    """
    Return all public galleries as an HTML ul element.
    """
    galleries = GalleryCustom.objects.filter(gallery__is_public=True) \
                                     .order_by('gallery__date_added')
    return {'galleries': galleries,
            'private_galleries_list': False}

def get_private_photo_galleries_array(user):
    galleries_private = GalleryCustom.objects.filter(gallery__is_public=False) \
                                             .order_by('gallery__date_added')
    if user.is_superuser:
        return galleries_private
    else:
        return [gal for gal in galleries_private if user in gal.allowed_users.all()]

@register.simple_tag(takes_context=True)
def get_private_photo_galleries_num(context):
    """
    Return the number of private galleries accessible to the user.
    """
    return len(get_private_photo_galleries_array(context['user']))

@register.inclusion_tag('photologue/tags/galleries.html', takes_context=True)
def get_private_photo_galleries(context):
    """
    Return all private galleries accessible to the user as an HTML ul element.
    """
    return {'galleries': get_private_photo_galleries_array(context['user']),
            'private_galleries_list': True,
            'user': context['user']}
