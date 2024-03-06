from dal.autocomplete import Select2QuerySetView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render

from critique.models import Artiste, Oeuvre


def detail_artiste(req, slug):
    artist = get_object_or_404(Artiste, slug=slug)
    oeuvres = Oeuvre.objects.filter(artists=artist).order_by('year')
    for oeuvre in oeuvres:
        if oeuvre.year == 2099:
            oeuvre.year = '20xx'
    context = {'oeuvres': oeuvres, 'artist': artist.name}
    return render(req, 'critique/artiste.html', context)


class ArtisteAutocomplete(PermissionRequiredMixin, Select2QuerySetView):
    permission_required = 'critique.all_rights'

    def get_queryset(self):
        qs = Artiste.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
