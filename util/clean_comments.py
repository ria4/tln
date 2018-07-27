import mongoengine
import time
from critique.models import Oeuvre

mongoengine.connect('critique_exp', alias='default')

print(len(Oeuvre.objects.all()))
time.sleep(1)

i = 1
for oeuvre in Oeuvre.objects.all():
    if oeuvre.comments:
        for comment in oeuvre.comments:
            comment.content = "\r\n\r\n".join(comment.content)
        oeuvre.save()
    print(i)
    i += 1
