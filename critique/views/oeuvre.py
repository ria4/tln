import binascii
import json
import os
import requests
import shutil

from dal.autocomplete import Select2QuerySetView
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import slugify
from PIL import Image

from critique.forms import OeuvreForm, OeuvreSpanForm, CommentaireForm
from critique.models import Artiste, Oeuvre, OeuvreTag
from critique.views.collection import cache_oeuvre_refresh
from critique.views.commentaire import get_comment_form_data
from critique.views.oeuvrespan import get_oeuvrespan_form_data


MAX_SPANS_ON_OEUVRE = 3


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
    spans = oeuvre.spans.all().order_by('-id')[:MAX_SPANS_ON_OEUVRE]
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


# Search

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
    oeuvres = Oeuvre.objects.none()
    if (len(match) >= 5):
        oeuvres = (
            Oeuvre.objects.filter(artists__name__icontains=match)
            .order_by('-year')[:limit]
        )
    oeuvres_n = len(oeuvres)
    if oeuvres_n == limit:
        return format_oeuvre_results(oeuvres, ajax)

    oeuvres_commentated = (
        Oeuvre.objects.filter(
            Q(comment__isnull=False) &
            (Q(title_vo__icontains=match) | Q(title_vf__icontains=match))
        ).order_by('-year')[:limit-oeuvres_n]
    )
    oeuvres |= oeuvres_commentated
    oeuvres_n = len(oeuvres)
    if oeuvres_n == limit:
        return format_oeuvre_results(oeuvres, ajax)

    oeuvres_uncommentated = (
        Oeuvre.objects.filter(
            Q(comment=None) &
            (Q(title_vo__icontains=match) | Q(title_vf__icontains=match))
        ).order_by('-year')[:limit-oeuvres_n]
    )
    oeuvres |= oeuvres_uncommentated
    return format_oeuvre_results(oeuvres, ajax)

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
