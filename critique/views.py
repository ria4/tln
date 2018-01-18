
import binascii
import os
import random
import requests
import shutil
from datetime import datetime
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OeuvreForm, OeuvreCommentForm, CinemaForm
from .models import Oeuvre, OeuvreComment, TopFilms, TopTextes, Cinema, Seance


# Préambule

def preambule(req):
    return render(req, 'critique/preambule.html', {})


# Artiste

def artiste(req, artist):
    oeuvres = Oeuvre.objects(__raw__={"$query": {'info.artists': artist},
                                      "$orderby": {'info.year': 1}})
    context = {'oeuvres': oeuvres, 'artist': artist}
    return render(req, 'critique/artiste.html', context)


# Oeuvre

# Helpers

def download_distant_image(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        h = binascii.hexlify(os.urandom(16))
        local_url = 'critique/%s' % h.decode('ascii')
        with open('critique/static/%s' % local_url, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            return local_url
    return ''

def get_oeuvre_form_data(oeuvre):
    form_data = {}
    form_data['type'] = oeuvre.info.type
    form_data['title_vf'] = oeuvre.info.titles.vf
    if hasattr(oeuvre.info.titles, 'vo'):
        form_data['title_vo'] = oeuvre.info.titles.vo
    if hasattr(oeuvre.info.titles, 'alt') and oeuvre.info.titles.alt:
        form_data['title_alt'] = '; '.join(list(oeuvre.info.titles.alt))
    form_data['artists'] = '; '.join(list(oeuvre.info.artists))
    form_data['year'] = oeuvre.info.year
    if hasattr(oeuvre.info, 'imdb_id'):
        form_data['imdb_id'] = oeuvre.info.imdb_id
    if hasattr(oeuvre, 'tags'):
        form_data['tags'] = oeuvre.tags
    if hasattr(oeuvre, 'envie'):
        form_data['envie'] = oeuvre.envie
    return form_data

@permission_required('critique.all_rights')
def update_oeuvre(req, oeuvre, form):
    oeuvre.info.type = form.cleaned_data['type']
    oeuvre.info.titles.vf = form.cleaned_data['title_vf']
    if form.cleaned_data['title_vo']:
        oeuvre.info.titles.vo = form.cleaned_data['title_vo']
    if form.cleaned_data['title_alt']:
        oeuvre.info.titles.alt = form.cleaned_data['title_alt'].split('; ')
    oeuvre.info.artists = form.cleaned_data['artists'].split('; ')
    oeuvre.info.year = form.cleaned_data['year']
    if form.cleaned_data['imdb_id']:
        oeuvre.info.imdb_id = form.cleaned_data['imdb_id']
    if form.cleaned_data['image_link']:
        url = download_distant_image(form.cleaned_data['image_link'])
        oeuvre.info.image_url = url
    if form.cleaned_data['tags']:
        oeuvre.tags = form.cleaned_data['tags']
    if 'envie' in form.cleaned_data:
        oeuvre.envie = form.cleaned_data['envie']
    oeuvre.save()

def get_comment_form_data(comment):
    form_data = {}
    form_data['title'] = comment.title
    form_data['date'] = comment.date.strftime('%Y-%m-%d')
    if hasattr(comment, 'date_month_unknown'):
        form_data['no_month'] = comment.date_month_unknown
    if hasattr(comment, 'date_day_unknown'):
        form_data['no_day'] = comment.date_day_unknown
    form_data['content'] = '\n\n'.join(comment.content)
    return form_data

@permission_required('critique.all_rights')
def update_latest_comment(req, id):
    comment_form = OeuvreCommentForm(req.POST)
    if req.POST and comment_form.is_valid():
        # actually there should already have been client-side validation
        oeuvre = get_object_or_404(Oeuvre, id=id)
        comments = sorted(oeuvre.comments, key=lambda p: p.date, reverse=True)
        update_comment_with_form(comments[0], comment_form)
        oeuvre.save()
    return redirect('detail_oeuvre', id=id)

def update_comment_with_form(comment, form):
    if form.cleaned_data['title']:
        comment.title = form.cleaned_data['title']
    comment.date = form.cleaned_data['date']
    if 'no_month' in form.cleaned_data:
        comment.date_month_unknown = form.cleaned_data['no_month']
    if 'no_day' in form.cleaned_data:
        comment.date_day_unknown = form.cleaned_data['no_day']
    comment.content = form.cleaned_data['content'].split('\r\n\r\n')

@permission_required('critique.all_rights')
def add_comment(req, id):
    """
    The id here should be an oeuvre.id.
    Note that 'comment' being an EmbeddedDocument, it cannot be saved as such.
    """
    form = OeuvreCommentForm(req.POST)
    if form.is_valid():
        comment = OeuvreComment()
        update_comment_with_form(comment, form)
        oeuvre = get_object_or_404(Oeuvre, id=id)
        if oeuvre.comments:
            oeuvre.comments.append(comment)
        else:
            oeuvre.comments = [comment]
        oeuvre.save()
    return redirect('detail_oeuvre', id=id)

# Views

@permission_required('critique.all_rights')
def add_oeuvre(req):
    form = OeuvreForm(req.POST)
    oeuvre = Oeuvre()
    if form.is_valid():
        update_oeuvre(req, oeuvre, form)
        return redirect('detail_oeuvre', id=oeuvre.id)

def detail_oeuvre(req, id):
    """
    We need to order the comments by date before sending them to the template.
    Only the most recent comment may be edited.
    """
    oeuvre = get_object_or_404(Oeuvre, id=id)
    oeuvre_form = OeuvreForm(req.POST or get_oeuvre_form_data(oeuvre))
    if req.POST and oeuvre_form.is_valid():
        # actually there should already have been client-side validation
        update_oeuvre(req, oeuvre, oeuvre_form)
    comments = comment_form = None
    if oeuvre.comments:
        comments = sorted(oeuvre.comments, key=lambda p: p.date, reverse=True)
        comment_form = OeuvreCommentForm(get_comment_form_data(comments[0]))
    return render(req, 'critique/oeuvre.html', locals())

def detail_oeuvre_slug(req, slug):
    try:
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
    except Oeuvre.MultipleObjectsReturned:
        oeuvres = Oeuvre.objects.filter(slug=slug)
        return render(req, 'critique/oeuvres.html', {'oeuvres': oeuvres})
    oeuvre_form = OeuvreForm(get_oeuvre_form_data(oeuvre))
    if oeuvre.comments:
        comments = sorted(oeuvre.comments, key=lambda p: p.date, reverse=True)
        comment_form = OeuvreCommentForm(get_comment_form_data(comments[0]))
    return render(req, 'critique/oeuvre.html', locals())

@permission_required('critique.all_rights')
def delete_oeuvre(req, id):
    oeuvre = get_object_or_404(Oeuvre, id=id)
    mtype = oeuvre.info.type
    oeuvre.delete()
    return redirect('list_oeuvres', mtype)

@permission_required('critique.all_rights')
def delete_latest_comment(req, id):
    oeuvre = get_object_or_404(Oeuvre, id=id)
    n = len(oeuvre.comments)
    comments = sorted(enumerate(oeuvre.comments),
                      key=lambda p: p[1].date, reverse=True)
    del(oeuvre.comments[comments[0][0]])
    oeuvre.save()
    return redirect('detail_oeuvre', id=id)


# Top Textes

def top_textes(req):
    top_textes = get_object_or_404(TopTextes)
    top_oeuvres = []
    for texte in top_textes.textes:
        content = texte.content
        oeuvre = Oeuvre.objects(__raw__={'comments.content': content})
        top_oeuvres.append((oeuvre[0], texte))
    return render(req, 'critique/top_textes.html', locals())


# Notes

def list_notes(req, mtype="all", page=1):
    if mtype == "all":
        oeuvres_list = Oeuvre.objects(__raw__={'comments.0': {'$exists': 'true'}})
    else:
        oeuvres_list = Oeuvre.objects(__raw__={'comments.0': {'$exists': 'true'}, 'info.type': mtype})
    oeuvres_list = oeuvres_list.order_by('-comments__date')
    paginator = Paginator(oeuvres_list, 20)
    try:
        oeuvres = paginator.page(page)
    except EmptyPage:
        oeuvres = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres, 'mtype': mtype}
    return render(req, 'critique/notes.html', context)


# Collection

def list_oeuvres(req, mtype, page=1):
    """
    Liste les oeuvres qui ne sont pas marquées en tant qu'envies.
    (Les "re-" envies ne sont pas prises en charge.)
    """
    oeuvres_list = Oeuvre.objects(__raw__={'envie': False, 'info.type': mtype})
    #paginator = Paginator(oeuvres_list, 20)
    #try:
    #    oeuvres = paginator.page(page)
    #except EmptyPage:
    #    oeuvres = paginator.page(paginator.num_pages)
    oeuvres = oeuvres_list.order_by('-info__year')
    context = {'oeuvres': oeuvres, 'mtype': mtype}
    return render(req, 'critique/collection.html', context)


# Envies

def list_envies(req, mtype, page=1):
    oeuvres_list = Oeuvre.objects(__raw__={'envie': True, 'info.type': mtype})
    paginator = Paginator(oeuvres_list, 22)
    try:
        oeuvres = paginator.page(page)
    except EmptyPage:
        oeuvres = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres, 'mtype': mtype}
    return render(req, 'critique/envies.html', context)


# Cinemas

# Helpers

def get_cinema_form_data(cinema):
    form_data = {}
    form_data['name'] = cinema.name
    form_data['comment'] = '\n\n'.join(cinema.comment)
    form_data['visited'] = cinema.visited.strftime('%Y-%m-%d')
    return form_data

@permission_required('critique.all_rights')
def update_cinema(req, cinema, form):
    cinema.name = form.cleaned_data['name']
    cinema.comment = form.cleaned_data['comment'].split('\r\n\r\n')
    cinema.visited = form.cleaned_data['visited']
    cinema.save()

# Views

def list_cinemas(req):
    cinemas = list(Cinema.objects.all())
    random.shuffle(cinemas)
    return render(req, 'critique/cinemas.html', {'cinemas': cinemas})

def detail_cinema(req, id):
    cinema = get_object_or_404(Cinema, id=id)
    form = CinemaForm(req.POST or get_cinema_form_data(cinema))
    if req.POST and form.is_valid():
        update_cinema(req, cinema, form)
    return render(req, 'critique/cinema.html', locals())

@permission_required('critique.all_rights')
def delete_cinema(req, id):
    cinema = get_object_or_404(Cinema, id=id).delete()
    return redirect('list_cinemas')


# Séances

def list_seances(req, year=2017):
    if year > 2011:
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    else:
        year = 2011
        start = datetime(2000, 1, 1)
        end = datetime(2011, 12, 31)
    seances = Seance.objects(__raw__={'date': {'$gte': start, '$lte': end}}).order_by('date')
    year_range = range(2012, 2018)
    return render(req, 'critique/seances.html', locals())


# Top Films

def top_films(req, year=2017):
    oeuvres = list(get_object_or_404(TopFilms, year=year).top)
    random.shuffle(oeuvres)
    year_range = range(2012, 2018)
    return render(req, 'critique/top_films.html', locals())


# Login

def login_view(req):
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    return redirect('preambule')

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
        return redirect('preambule')
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

