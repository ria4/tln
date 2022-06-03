import django
django.setup()

from django.core.files.base import File
from critique.models import Oeuvre


for i, o in enumerate(Oeuvre.objects.all()):
    if o.image_url:
        filename = o.image_url[9:] 
        filepath = '/home/ria/tln/media/oeuvre_imgs/' + filename
        try:
            with open(filepath, 'rb') as f:
                o.image.save(filename, File(f))
        except FileNotFoundError:
            print(o.title_vf)
            continue
    print(i)
