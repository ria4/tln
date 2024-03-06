import binascii
import json
import logging
import os
import requests
import shutil

from dal.autocomplete import Select2QuerySetView
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files import File
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from PIL import Image

from critique.constants import MAX_SPANS_ON_OEUVRE, OEUVRES_IMG_TMP_DIR
from critique.forms import OeuvreForm, OeuvreSpanForm, CommentaireForm
from critique.models import Artiste, Oeuvre, OeuvreTag
from critique.views.collection import refresh_oeuvre_cache_threaded
from critique.views.commentaire import get_comment_form_data
from critique.views.oeuvrespan import get_oeuvrespan_form_data


logger = logging.getLogger('django')


# Helpers

def download_distant_image(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        h = binascii.hexlify(os.urandom(16))
        imagename = h.decode('ascii')
        preimagepath = f'{OEUVRES_IMG_TMP_DIR}/{imagename}'
        with open(preimagepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        baseheight = 300
        with Image.open(preimagepath) as image:
            if image.format == 'JPEG':
                imagename += '.jpg'
                imagepath = f'{preimagepath}.jpg'
            elif image.format == 'PNG':
                imagename += '.png'
                imagepath = f'{preimagepath}.png'
            else:
                logger.warning(f"Unknown format for image at {url}: {r.content}")
                os.remove(preimagepath)
                return None, None
            hpercent = baseheight/float(image.size[1])
            wsize = int(float(image.size[0])*float(hpercent))
            image = image.resize((wsize, baseheight), Image.LANCZOS)
            image.save(imagepath)
        os.remove(preimagepath)
        return imagename, imagepath
    else:
        logger.warning(f"Failed to download image at {url}: {r.content}")
        return None, None

def get_oeuvre_form_data(oeuvre):
    form_data = {}
    form_data['mtype'] = oeuvre.mtype
    form_data['title_vf'] = oeuvre.title_vf
    form_data['title_vo'] = oeuvre.title_vo
    form_data['title_alt'] = oeuvre.title_alt
    form_data['artists'] = oeuvre.artists.all()
    form_data['year'] = oeuvre.year
    form_data['imdb_id'] = oeuvre.imdb_id
    form_data['tags'] = oeuvre.tags.all()
    form_data['envie'] = oeuvre.envie
    return form_data


# Views

@permission_required('critique.all_rights')
def add_oeuvre(req):
    form = OeuvreForm(req.POST)
    if form.is_valid():
        oeuvre = Oeuvre()
        update_oeuvre(req, oeuvre, form)
        refresh_oeuvre_cache_threaded(oeuvre.mtype)
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
        imagename, imagepath = download_distant_image(form.cleaned_data['image_link'])
        if imagename and imagepath:
            if oeuvre.image:
                oeuvre.image.delete()
            with open(imagepath, 'rb') as image:
                oeuvre.image.save(imagename, File(image), save=False)
            os.remove(imagepath)
    oeuvre.envie = form.cleaned_data['envie']
    oeuvre.save(update_slug=update_slug)

    artists = form.cleaned_data['artists']
    oeuvre.artists.set(artists)
    tags = form.cleaned_data['tags']
    oeuvre.tags.set(tags)

@permission_required('critique.all_rights')
def delete_oeuvre(req, slug):
    oeuvre = get_object_or_404(Oeuvre.objects.prefetch_related('tags'), slug=slug)
    # delete image if applicable
    if hasattr(oeuvre, 'image_url') and oeuvre.image_url:
        #XXX put this in Oeuvre.delete when it's reworked
        try:
            os.remove('static/%s' % oeuvre.image_url)
        except FileNotFoundError:
            pass
    # delete unused tags if applicable
    for tag in (
        OeuvreTag.objects.filter(id__in=oeuvre.tags.all())
        .annotate(cnt=Count('oeuvre'))
        .filter(cnt=1)
    ):
        tag.delete()
    # finally, delete oeuvre
    oeuvre.delete()
    return redirect('list_oeuvres', oeuvre.mtype)

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
        span_form = OeuvreSpanForm(initial=get_oeuvrespan_form_data(spans[0]))
        span_form.fields["ongoing"].widget.attrs.update({"class": "focus-on-reveal"})
    # clear previous order_by
    spans = sorted(spans, key=lambda os: os.date_start)
    long_span = any([span.date_start.month >= 9 for span in spans])
    comments = oeuvre.comments.all().order_by('-date')
    comment_form = None
    if comments:
        comment_form = CommentaireForm(get_comment_form_data(comments[0]))
        comment_form.fields["content"].widget.attrs.update({"class": "focus-on-reveal"})
    if req.POST:
        oeuvre_form = OeuvreForm(req.POST)
    else:
        oeuvre_form = OeuvreForm(initial=get_oeuvre_form_data(oeuvre))
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

    if req.headers.get('x-requested-with') == 'XMLHttpRequest':
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


class OeuvreTagAutocomplete(PermissionRequiredMixin, Select2QuerySetView):
    permission_required = 'critique.all_rights'
    paginate_by = 30  # equivalent to pagination off

    def get_queryset(self):
        qs = OeuvreTag.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
