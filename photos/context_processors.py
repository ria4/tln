from .models import GalleryCustom

def gallery_list(req):
    gallery_list = GalleryCustom.objects.filter(gallery__is_public=True).order_by("gallery__date_added")
    return {"gallery_list": gallery_list}
