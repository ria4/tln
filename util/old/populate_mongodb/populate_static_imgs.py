
import mongoengine, sys
from critique.models import *


mongoengine.connect('critique_django', alias='default')

for i, item in enumerate(Oeuvre.objects.all()):
    try:
        if item.info.image and item.info.image.md5:
            url = create_image_url(item.info.image)
            item.info.image_url = url
            item.save()
        vf = item.info.titles.vf
        print(i, vf, url)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

