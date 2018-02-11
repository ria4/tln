from photologue.models import Gallery

def gallery_list(req):
    gallery_list = Gallery.objects.on_site().is_public().order_by("date_added")
    return {"gallery_list": gallery_list}
