import datetime
import random

from dal.autocomplete import Select2QuerySetView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import prefetch_related_objects, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render

from critique.forms import CinemaForm
from critique.models import Cinema, Seance


# Helpers

def get_cinema_form_data(cinema):
    form_data = {}
    form_data['name'] = cinema.name
    form_data['name_short'] = cinema.name_short
    form_data['name_long'] = cinema.name_long
    form_data['location'] = cinema.location
    form_data['comment'] = cinema.comment
    if cinema.visited:
        visited = cinema.visited.strftime('%Y-%m-%d')
        form_data['visited'] = visited if visited != '1970-01-01' else None
    else:
        form_data['visited'] = None
    return form_data


# Autocomplete

class CinemaAutocomplete(PermissionRequiredMixin, Select2QuerySetView):
    permission_required = 'critique.all_rights'

    def get_queryset(self):
        qs = Cinema.objects.exclude(
            Q(name="UGC") | Q(name="MK2")
        )
        if self.q:
            qs = qs.filter(name__icontains=self.q).order_by("name")
        return qs


# Views

@permission_required('critique.all_rights')
def update_cinema(req, cinema, form):
    update_slug = form.cleaned_data['name'] != cinema.name
    cinema.name = form.cleaned_data['name']
    name_short = form.cleaned_data['name_short']
    cinema.name_short = name_short if name_short else None
    cinema.name_long = form.cleaned_data['name_long']
    cinema.location = form.cleaned_data['location']
    cinema.comment = form.cleaned_data['comment']
    visited = form.cleaned_data['visited']
    cinema.visited = visited if visited != datetime.date.fromtimestamp(0) else None
    cinema.save(update_slug=update_slug)

@permission_required('critique.all_rights')
def add_cinema(req):
    form = CinemaForm(req.POST)
    if form.is_valid():
        cinema = Cinema()
        update_cinema(req, cinema, form)
        return redirect('list_cinemas')

def list_cinemas(req):
    """
    L'ordre des cinémas est aléatoire, mais constant pour un jour donné.
    """
    cinemas_paris_q = Cinema.objects.filter(location__startswith="Paris").exclude(
        Q(name="UGC") | Q(name="MK2") | Q(comment="")
    )
    cinemas_paris = list(cinemas_paris_q)
    random.seed(datetime.datetime.today().date())
    random.shuffle(cinemas_paris)
    cinemas_elsewhere_q = (
        Cinema.objects.exclude(
            Q(name="UGC") | Q(name="MK2") | Q(location__startswith="Paris")
        ).order_by('location')
        .values('name', 'location', 'slug')
    )
    context = {'cinemas_paris': cinemas_paris, 'cinemas_elsewhere': cinemas_elsewhere_q}
    return render(req, 'critique/cinemas.html', context)

def detail_cinema(req, slug):
    cinema = get_object_or_404(Cinema, slug=slug)
    prefetch_related_objects(
        [cinema],
        Prefetch(
            'seances',
            queryset=(
                Seance.objects.select_related('oeuvre_span')
                .order_by('oeuvre_span__date_start')
            ),
            to_attr='seances_list',
        )
    )
    form = CinemaForm(req.POST or get_cinema_form_data(cinema))
    form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST and form.is_valid():
        update_cinema(req, cinema, form)
        return redirect('detail_cinema', slug=cinema.slug)
    # optimize chunk columns balance
    r = len(cinema.seances_list) % 10
    chunk_size = 10
    if 1 <= r <= 3:
        chunk_size += 1
    return render(req, 'critique/cinema.html', locals())

@permission_required('critique.all_rights')
def delete_cinema(req, slug):
    cinema = get_object_or_404(Cinema, slug=slug).delete()
    return redirect('list_cinemas')
