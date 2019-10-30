import mongoengine
from django.template.defaultfilters import slugify
from critique.models import Oeuvre, Seance

mongoengine.connect('critique_django', alias='default')
seances = Seance.objects.all().order_by('date')

n = 0
i = 1
for seance in seances:
    if seance.film:
        slug = slugify(seance.film)
        films = Oeuvre.objects.filter(slug=slug)
        if len(films) > 0:
            film = films[0]
            if len(Seance.objects.filter(film_id=str(film.id))) == 0:
                seance.date_month_unknown = seance.date_day_unknown
                seance.film_id = str(film.id)
                seance.save()
            n += 1
        else:
            print()
            print(seance.film)
            print("db.oeuvre.find({slug:")
            print("},{_id:1}).forEach(function(doc){db.seance.update({_id:ObjectId('%s')}, {$set: {film_id: doc._id.str}})})" % seance.id)
    i += 1
