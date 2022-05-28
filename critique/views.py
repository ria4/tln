import binascii
import json
import os
import pytz
import random
import requests
import shutil

from dal.autocomplete import Select2QuerySetView
from datetime import datetime, date, time
from itertools import chain
from PIL import Image
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Max, prefetch_related_objects, Prefetch, Q
from django.db.models.functions import Length
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic.list import ListView

from .forms import (
    OeuvreForm,
    OeuvreSpanForm,
    CommentaireForm,
    CinemaForm,
    SeanceForm,
)
from .models import (
    Artiste,
    Oeuvre,
    OeuvreSpan,
    OeuvreTag,
    Commentaire,
    TopFilms,
    TopJeux,
    Cinema,
    Seance,
)


def strftime_local(dt):
    return dt.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d')


# Artiste

def detail_artiste(req, slug):
    artist = get_object_or_404(Artiste, slug=slug)
    oeuvres = Oeuvre.objects.filter(artists=artist).order_by('year')
    for oeuvre in oeuvres:
        if oeuvre.year == 2099:
            oeuvre.year = '20xx'
    context = {'oeuvres': oeuvres, 'artist': artist.name}
    return render(req, 'critique/artiste.html', context)


# Oeuvre

# Helpers

def download_distant_image(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        h = binascii.hexlify(os.urandom(16))
        local_url = h.decode('ascii')
        with open('static/critique/tmp/%s' % local_url, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        baseheight = 300
        img = Image.open('static/critique/tmp/%s' % local_url)
        fmt = 'jpg'
        if img.format == 'PNG':
            fmt = 'png'
        hpercent = baseheight/float(img.size[1])
        wsize = int(float(img.size[0])*float(hpercent))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save('static/critique/%s.%s' % (local_url, fmt))
        os.remove('static/critique/tmp/%s' % local_url)
        return 'critique/%s.%s' % (local_url, fmt)
    return ''

def get_oeuvre_form_data(oeuvre):
    form_data = {}
    form_data['mtype'] = oeuvre.mtype
    form_data['title_vf'] = oeuvre.title_vf
    form_data['title_vo'] = oeuvre.title_vo
    form_data['title_alt'] = oeuvre.title_alt
    names = [artist.name for artist in oeuvre.artists.all()]
    form_data['artists'] = '; '.join(names)
    form_data['year'] = oeuvre.year
    form_data['imdb_id'] = oeuvre.imdb_id
    tags = [tag.name for tag in oeuvre.tags.all()]
    form_data['tags'] = '; '.join(tags)
    form_data['envie'] = oeuvre.envie
    return form_data

@permission_required('critique.all_rights')
def update_oeuvre(req, oeuvre, form):
    oeuvre.mtype = form.cleaned_data['mtype']
    update_slug = form.cleaned_data['title_vf'] != oeuvre.title_vf
    oeuvre.title_vf = form.cleaned_data['title_vf']
    oeuvre.title_vo = form.cleaned_data['title_vo']
    oeuvre.title_alt = form.cleaned_data['title_alt']
    oeuvre.year = form.cleaned_data['year']
    oeuvre.imdb_id = form.cleaned_data['imdb_id']
    if form.cleaned_data['image_link']:
        url = download_distant_image(form.cleaned_data['image_link'])
        if oeuvre.image_url:
            try:
                os.remove('static/%s' % oeuvre.image_url)
            except FileNotFoundError:
                pass
        oeuvre.image_url = url
    oeuvre.envie = form.cleaned_data['envie']
    oeuvre.save(update_slug=update_slug)

    artists_names = form.cleaned_data['artists'].split('; ')
    artists = []
    for artist_name in artists_names:
        artist, _ = Artiste.objects.get_or_create(
            name=artist_name,
            slug=slugify(artist_name),
        )
        artists.append(artist)
    oeuvre.artists.set(artists)
    tags = []
    tags_names = []
    if form.cleaned_data['tags']:
        tags_names = form.cleaned_data['tags'].split('; ')
    for tag_name in tags_names:
        tag, _ = OeuvreTag.objects.get_or_create(name=tag_name)
        tags.append(tag)
    oeuvre.tags.set(tags)

def get_comment_form_data(comment):
    form_data = {}
    form_data['title'] = comment.title
    form_data['date'] = strftime_local(comment.date)
    if hasattr(comment, 'date_month_unknown'):
        form_data['no_month'] = comment.date_month_unknown
    if hasattr(comment, 'date_day_unknown'):
        form_data['no_day'] = comment.date_day_unknown
    form_data['content'] = comment.content
    return form_data

@permission_required('critique.all_rights')
def update_latest_comment(req, slug):
    comment_form = CommentaireForm(req.POST)
    if req.POST and comment_form.is_valid():
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        comments = sorted(oeuvre.comments.all(), key=lambda p: p.date, reverse=True)
        update_comment_with_form(comments[0], comment_form)
    return redirect('detail_oeuvre', slug=slug)

def update_comment_with_form(comment, form):
    comment.title = form.cleaned_data['title']
    dt = datetime.combine(form.cleaned_data['date'], datetime.now().time())
    comment.date = dt.replace(microsecond=0)
    comment.date_month_unknown = form.cleaned_data['no_month']
    comment.date_day_unknown = form.cleaned_data['no_day']
    comment.content = form.cleaned_data['content']
    comment.save()

@permission_required('critique.all_rights')
def add_comment(req, slug):
    form = CommentaireForm(req.POST)
    if form.is_valid():
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        comment = Commentaire(oeuvre=oeuvre)
        update_comment_with_form(comment, form)
        oeuvre.comments.add(comment)
    return redirect('detail_oeuvre', slug=slug)


# Oeuvre Cache

def cache_oeuvre_refresh(mtype):
    cache_key = make_template_fragment_key('chunks_collection', [mtype])
    cache.delete(cache_key)
    context = list_oeuvres_reqless(mtype)
    render_to_string('critique/collection.html', context=context)
    # close connection if in another thread
    #from django.db import connection
    #connection.close()

#import threading
#
#def cache_oeuvre_refresh_thread(mtype):
#    t = threading.Thread(
#        target=cache_oeuvre_refresh,
#        args=[mtype],
#        daemon=True,
#    )
#    t.start()


# Views

@permission_required('critique.all_rights')
def add_oeuvre(req):
    form = OeuvreForm(req.POST)
    if form.is_valid():
        oeuvre = Oeuvre()
        update_oeuvre(req, oeuvre, form)
        # refresh cache
        # "To provide thread-safety, a different instance"
        # "of the cache backend will be returned for each thread."
        # https://docs.djangoproject.com/en/4.0/topics/cache/#cache-key-prefixing
        #cache_oeuvre_refresh_thread(oeuvre.mtype)
        cache_oeuvre_refresh(oeuvre.mtype)
        return redirect('detail_oeuvre', slug=oeuvre.slug)

def detail_oeuvre(req, slug):
    """
    We need to order the comments by date before sending them
    to the template. Only the most recent comment may be edited.
    """
    oeuvre = get_object_or_404(
        Oeuvre.objects.prefetch_related(
            'spans',
            'spans__seance',
            'spans__seance__cinema',
            'comments',
        ),
        slug=slug,
    )
    spans = oeuvre.spans.all().order_by('-id')
    if spans:
        span_form = OeuvreSpanForm(get_oeuvrespan_form_data(spans[0]))
        span_form.fields["ongoing"].widget.attrs.update({"class": "focus-on-reveal"})
    # clear previous order_by
    spans = sorted(spans, key=lambda os: os.date_start)
    comments = oeuvre.comments.all().order_by('-date')
    comment_form = None
    if comments:
        comment_form = CommentaireForm(get_comment_form_data(comments[0]))
        comment_form.fields["content"].widget.attrs.update({"class": "focus-on-reveal"})
    oeuvre_form = OeuvreForm(req.POST or get_oeuvre_form_data(oeuvre))
    oeuvre_form.fields["envie"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST and oeuvre_form.is_valid():
        # actually there should already have been client-side validation
        update_oeuvre(req, oeuvre, oeuvre_form)
        # we redirect because the slug might change
        return redirect('detail_oeuvre', slug=oeuvre.slug)
    if oeuvre.year == 2099:
        oeuvre.year = '20xx'
    return render(req, 'critique/oeuvre.html', locals())

@permission_required('critique.all_rights')
def delete_oeuvre(req, slug):
    oeuvre = get_object_or_404(Oeuvre, slug=slug)
    mtype = oeuvre.mtype
    if hasattr(oeuvre, 'image_url') and oeuvre.image_url:
        #XXX put this in Oeuvre.delete when it's reworked
        try:
            os.remove('static/%s' % oeuvre.image_url)
        except FileNotFoundError:
            pass
    oeuvre.delete()
    return redirect('list_oeuvres', mtype)

@permission_required('critique.all_rights')
def delete_latest_comment(req, slug):
    oeuvre = get_object_or_404(
        Oeuvre.objects.select_related('comments').order_by('-comment__date'),
        slug=slug,
    )
    if oeuvre.comments:
        oeuvre.comments[0].delete()
    return redirect('detail_oeuvre', slug=slug)


# Search Oeuvres

def format_oeuvre_results(oeuvres, ajax):
    if ajax:
        res = [ {'vf': oeuvre.title_vf,
                 'vo': oeuvre.title_vo,
                 'year': oeuvre.year,
                 'slug': oeuvre.slug} for oeuvre in oeuvres ]
        for info in res:
            if info["year"] == 2099:
                info["year"] = "20xx"
        return json.dumps(res)
    else:
        for oeuvre in oeuvres:
            if oeuvre.year == 2099:
                oeuvre.year = "20xx"
        return oeuvres

def get_oeuvres(match, limit, ajax=False):
    artiste = Artiste.objects.filter(name__iexact=match)
    if artiste:
        oeuvres = artiste[0].oeuvres.order_by('-year')[:limit]
        return format_oeuvre_results(oeuvres, ajax)
    else:
        oeuvres = (
            Oeuvre.objects.filter(
                Q(comment__isnull=False) &
                (Q(title_vo__icontains=match) | Q(title_vf__icontains=match))
            ).order_by('-comment__date')[:limit]
        )
        oeuvres_commentated_n = oeuvres.count()
        if oeuvres.count() == limit:
            return format_oeuvre_results(oeuvres, ajax)
        else:
            oeuvres_uncommentated = (
                Oeuvre.objects.filter(
                    Q(comment=None) &
                    (Q(title_vo__icontains=match) | Q(title_vf__icontains=match))
                ).order_by('-year')[:limit-oeuvres_commentated_n]
            )
            oeuvres_concat = list(chain(oeuvres, oeuvres_uncommentated))
            return format_oeuvre_results(oeuvres_concat, ajax)

def search_oeuvres(req, match=''):
    get_match = req.GET.get('match', None)
    if get_match is not None:
        if get_match:
            return redirect('search_oeuvres', match=get_match)
        else:
            return redirect('search_oeuvres')

    if req.is_ajax():
        oeuvres = get_oeuvres(match, 5, ajax=True)
        return HttpResponse(oeuvres)
    else:
        oeuvres = get_oeuvres(match, 10)
        return render(req, 'critique/search_oeuvres.html', locals())


# Autocomplete

class OeuvreAutocomplete(PermissionRequiredMixin, Select2QuerySetView):
    permission_required = 'critique.all_rights'

    def get_queryset(self):
        qs = Oeuvre.objects.all()
        if self.q:
            qs = qs.filter(
                Q(title_vo__icontains=self.q) | Q(title_vf__icontains=self.q)
            )
        return qs


class FilmAutocomplete(OeuvreAutocomplete):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(mtype='film')


# OeuvreSpan

@permission_required('critique.all_rights')
def add_oeuvrespan(req):
    form = OeuvreSpanForm(req.POST)
    oeuvre_span = OeuvreSpan()
    if form.is_valid():
        update_oeuvrespan(req, oeuvre_span, form)
        return redirect('detail_oeuvre', slug=oeuvre_span.oeuvre.slug)

@permission_required('critique.all_rights')
def update_oeuvrespan(req, oeuvre_span, form):
    oeuvre_span.date_start = form.cleaned_data.get('date_start')
    oeuvre_span.dsdu = form.cleaned_data.get('dsdu', False)
    oeuvre_span.date_end = form.cleaned_data.get('date_end')
    oeuvre_span.dedu = form.cleaned_data.get('dedu', False)
    oeuvre_span.oeuvre = form.cleaned_data.get('oeuvre')
    oeuvre_span.ongoing = form.cleaned_data.get('ongoing', False)
    oeuvre_span.save()

def update_oeuvrespan_with_form(oeuvrespan, form):
    oeuvrespan.oeuvre = form.cleaned_data['oeuvre']
    oeuvrespan.date_start = form.cleaned_data['date_start']
    oeuvrespan.dsdu = form.cleaned_data['dsdu']
    oeuvrespan.date_end = form.cleaned_data['date_end']
    oeuvrespan.dedu = form.cleaned_data['dedu']
    oeuvrespan.ongoing = form.cleaned_data['ongoing']
    oeuvrespan.save()

@permission_required('critique.all_rights')
def update_latest_oeuvrespan(req, slug):
    oeuvrespan_form = OeuvreSpanForm(req.POST)
    if req.POST and oeuvrespan_form.is_valid():
        span = OeuvreSpan.objects.filter(oeuvre__slug=slug).order_by('-id').first()
        update_oeuvrespan_with_form(span, oeuvrespan_form)
    return redirect('detail_oeuvre', slug=slug)

@permission_required('critique.all_rights')
def delete_latest_oeuvrespan(req, slug):
    oeuvrespans = OeuvreSpan.objects.filter(oeuvre__slug=slug).order_by('-id')
    if not oeuvrespans.exists():
        raise Http404
    oeuvrespan = oeuvrespans.first()
    slug = oeuvrespan.oeuvre.slug
    oeuvrespan.delete()
    return redirect('detail_oeuvre', slug=slug)

def get_oeuvrespan_form_data(oeuvrespan):
    form_data = {}
    if hasattr(oeuvrespan, 'oeuvre'):
        form_data['oeuvre'] = oeuvrespan.oeuvre;
    form_data['date_start'] = strftime_local(oeuvrespan.date_start)
    form_data['dsdu'] = oeuvrespan.dsdu
    form_data['date_end'] = strftime_local(oeuvrespan.date_end)
    form_data['dedu'] = oeuvrespan.dedu
    form_data['ongoing'] = oeuvrespan.ongoing
    return form_data


# Top Textes

class TopTextesView(ListView):
    queryset = Commentaire.objects.filter(starred=True).order_by('-date')
    template_name = 'critique/top_textes.html'


# Notes

def list_notes(req, mtype="all", page=1):
    if mtype == "all":
        notes_full = Commentaire.objects.annotate(content_len=Length('content')) \
                                        .filter(content_len__gt=400)
    else:
        notes_full = Commentaire.objects.filter(oeuvre__mtype=mtype) \
                                        .annotate(content_len=Length('content')) \
                                        .filter(content_len__gt=400)
    notes_full = notes_full.order_by('-date')
    paginator = Paginator(notes_full, 20)
    try:
        notes = paginator.page(page)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    context = {'notes': notes, 'mtype': mtype}
    return render(req, 'critique/notes.html', context)


# Collection

def list_oeuvres_reqless(mtype):
    oeuvres = Oeuvre.objects.filter(envie=False, mtype=mtype) \
                            .order_by('-year', '-id')
    return {'oeuvres': oeuvres, 'mtype': mtype}

def list_oeuvres(req, mtype="film"):
    """
    Liste les oeuvres qui ne sont pas marquées en tant qu'envies.
    (Les "re-" envies ne sont pas prises en charge.)
    """
    context = list_oeuvres_reqless(mtype)
    return render(req, 'critique/collection.html', context)


# Envies

def list_envies(req, mtype="film", page=1):
    oeuvres_list = Oeuvre.objects.filter(envie=True, mtype=mtype)
    oeuvres = oeuvres_list.order_by('-year', '-id')
    paginator = Paginator(oeuvres, 22)
    try:
        oeuvres_page = paginator.page(page)
    except EmptyPage:
        oeuvres_page = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres_page, 'mtype': mtype}
    return render(req, 'critique/envies.html', context)


# Tags

def list_tags(req):
    tags = OeuvreTag.objects.all()
    return render(req, 'critique/tags.html', {'tags': tags})

def detail_tag(req, slug, page=1):
    tag = get_object_or_404(OeuvreTag, slug=slug)
    oeuvres_list = Oeuvre.objects.filter(tags=tag)
    oeuvres = oeuvres_list.order_by('-year', '-id')
    paginator = Paginator(oeuvres, 22)
    try:
        oeuvres_page = paginator.page(page)
    except EmptyPage:
        oeuvres_page = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres_page, 'tag': tag.name}
    return render(req, 'critique/tag.html', context)


# Cinemas

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
    cinema.visited = visited if visited != date.fromtimestamp(0) else None
    cinema.save(update_slug=update_slug)

# Views

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
    random.seed(datetime.today().date())
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


# Séances

@permission_required('critique.all_rights')
def update_seance(req, seance, data):
    if not (data.get('film') or data.get('seance_title')):
        return

    if data.get('film'):
        oeuvre = data.get('film')
    else:
        oeuvre = None
        seance.seance_title = data['seance_title']

    date = data['date']
    dtime = time(int(data['hour'][:2]), int(data['hour'][3:5]))
    date_start = datetime.combine(date, dtime)

    span = OeuvreSpan(
        oeuvre=oeuvre,
        date_start=date_start,
        dsdu=data.get('no_day', False),
        dsmu=data.get('no_month', False),
        date_end=date_start,
        dedu=data.get('no_day', False),
        demu=data.get('no_month', False),
    )
    span.save()

    seance.oeuvre_span = span
    seance.cinema = data['cinema']
    seance.save()

@permission_required('critique.all_rights')
def add_seance(req):
    form = SeanceForm(req.POST)
    seance = Seance()
    if form.is_valid():
        update_seance(req, seance, form.cleaned_data)
        return redirect('list_seances', year=seance.oeuvre_span.date_start.year)

def list_seances(req, year=2022):
    form = SeanceForm(req.POST)
    if req.POST and form.is_valid():
        update_seances(req, form)

    if year > 2011:
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    else:
        year = 2011
        start = datetime(1998, 1, 1)
        end = datetime(2011, 12, 31)
    seances = (
        Seance.objects.filter(
            oeuvre_span__date_start__gte=start,
            oeuvre_span__date_start__lte=end,
        ).select_related(
            'cinema',
            'oeuvre_span',
        ).order_by('oeuvre_span__date_start')
    )

    return render(req, 'critique/seances.html', {'year': year, 'seances': seances})


# Top Films

def top_films(req, year=2011):
    oeuvres = list(get_object_or_404(TopFilms, year=year).films.all())
    random.shuffle(oeuvres)
    return render(req, 'critique/top_films.html', locals())


# Top Jeux

def top_jeux(req, year=2021):
    oeuvres = list(get_object_or_404(TopJeux, year=year).jeux.all())
    random.shuffle(oeuvres)
    return render(req, 'critique/top_jeux.html', locals())
