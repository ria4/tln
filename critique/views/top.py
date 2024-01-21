import random

from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView

from critique.models import Commentaire, TopFilms, TopJeux


# Top Textes

class TopTextesView(ListView):
    queryset = Commentaire.objects.filter(starred=True).order_by('-date')
    template_name = 'critique/top_textes.html'


# Top Films

def top_films(req, year=2011):
    oeuvres = list(get_object_or_404(TopFilms, year=year).films.all())
    random.shuffle(oeuvres)
    return render(req, 'critique/top_films.html', locals())


# Top Jeux

def top_jeux(req, year=2023):
    oeuvres = list(get_object_or_404(TopJeux, year=year).jeux.all())
    random.shuffle(oeuvres)
    return render(req, 'critique/top_jeux.html', locals())
