import binascii
import os
import random
import requests
import shutil
from datetime import datetime, time
from PIL import Image
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OeuvreForm, OeuvreCommentForm, CinemaForm, SeanceForm
from .models import Oeuvre, OeuvreComment, TopFilms, TopTextes, Cinema, Seance


# Préambule

def preambule(req):
    return render(req, 'critique/preambule.html', {})


# Artiste

def artiste(req, artist):
    oeuvres = Oeuvre.objects(__raw__={'$query': {'info.artists': artist},
                                      '$orderby': {'info.year': 1}})
    if len(oeuvres) == 0:
        raise Http404
    context = {'oeuvres': oeuvres, 'artist': artist}
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
        hpercent = baseheight/float(img.size[1])
        wsize = int(float(img.size[0])*float(hpercent))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save('static/critique/%s.jpg' % local_url)
        os.remove('static/critique/tmp/%s' % local_url)
        return 'critique/%s.jpg' % local_url
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
    else:
        oeuvre.info.titles.vo = None
    if form.cleaned_data['title_alt']:
        oeuvre.info.titles.alt = form.cleaned_data['title_alt'].split('; ')
    else:
        oeuvre.info.titles.alt = None
    oeuvre.info.artists = form.cleaned_data['artists'].split('; ')
    oeuvre.info.year = form.cleaned_data['year']
    if form.cleaned_data['imdb_id']:
        oeuvre.info.imdb_id = form.cleaned_data['imdb_id']
    else:
        oeuvre.info.imdb_id = None
    if form.cleaned_data['image_link']:
        url = download_distant_image(form.cleaned_data['image_link'])
        if oeuvre.info.image_url:
            try:
                os.remove('static/%s' % oeuvre.info.image_url)
            except FileNotFoundError:
                pass
        oeuvre.info.image_url = url
    if form.cleaned_data['tags']:
        oeuvre.tags = form.cleaned_data['tags']
    else:
        oeuvre.tags = None
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
def update_latest_comment(req, slug):
    comment_form = OeuvreCommentForm(req.POST)
    if req.POST and comment_form.is_valid():
        # actually there should already have been client-side validation
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        comments = sorted(oeuvre.comments, key=lambda p: p.date, reverse=True)
        update_comment_with_form(comments[0], comment_form)
        oeuvre.save()
    return redirect('detail_oeuvre', slug=slug)

def update_comment_with_form(comment, form):
    if form.cleaned_data['title']:
        comment.title = form.cleaned_data['title']
    else:
        comment.title = None
    comment.date = form.cleaned_data['date']
    if 'no_month' in form.cleaned_data:
        comment.date_month_unknown = form.cleaned_data['no_month']
    if 'no_day' in form.cleaned_data:
        comment.date_day_unknown = form.cleaned_data['no_day']
    comment.content = form.cleaned_data['content'].split('\r\n\r\n')

@permission_required('critique.all_rights')
def add_comment(req, slug):
    """
    Note that 'comment' being an EmbeddedDocument, it cannot be saved as such.
    """
    form = OeuvreCommentForm(req.POST)
    if form.is_valid():
        comment = OeuvreComment()
        update_comment_with_form(comment, form)
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
        if oeuvre.comments:
            oeuvre.comments.append(comment)
        else:
            oeuvre.comments = [comment]
        oeuvre.save()
    return redirect('detail_oeuvre', slug=slug)

# Views

@permission_required('critique.all_rights')
def add_oeuvre(req):
    form = OeuvreForm(req.POST)
    oeuvre = Oeuvre()
    if form.is_valid():
        update_oeuvre(req, oeuvre, form)
        return redirect('detail_oeuvre', slug=oeuvre.slug)

def render_oeuvre(req, oeuvre):
    """
    We need to order the comments by date before sending them to the template.
    For now, only the most recent comment may be edited.
    """
    if oeuvre.comments:
        comments = sorted(oeuvre.comments, key=lambda p: p.date, reverse=True)
        comment_form = OeuvreCommentForm(get_comment_form_data(comments[0]))
    oeuvre_form = OeuvreForm(req.POST or get_oeuvre_form_data(oeuvre))
    if req.POST and oeuvre_form.is_valid():
        # actually there should already have been client-side validation
        update_oeuvre(req, oeuvre, oeuvre_form)
        # we redirect just because the slug might change
        return redirect('detail_oeuvre', slug=oeuvre.slug)
    return render(req, 'critique/oeuvre.html', locals())

def detail_oeuvre(req, slug):
    oeuvres = Oeuvre.objects.filter(slug=slug)
    if len(oeuvres) == 1:
        return render_oeuvre(req, oeuvres[0])
    elif len(oeuvres) == 0:
        pattern = '^%s-\d+' % slug
        oeuvres = Oeuvre.objects(__raw__={'$query': {'slug': {'$regex': pattern}},
                                          '$orderby': {'info.year': -1}})
        if len(oeuvres) > 0:
            return render(req, 'critique/oeuvres.html', {'oeuvres': oeuvres})
        raise Http404
    elif len(oeuvres) > 1:
        # the slug field should be unique
        return HttpResponseServerError()

@permission_required('critique.all_rights')
def delete_oeuvre(req, slug):
    oeuvre = get_object_or_404(Oeuvre, slug=slug)
    mtype = oeuvre.info.type
    if hasattr(oeuvre.info, 'image_url') and oeuvre.info.image_url:
        try:
            os.remove('static/%s' % oeuvre.info.image_url)
        except FileNotFoundError:
            pass
    oeuvre.delete()
    return redirect('list_oeuvres', mtype)

@permission_required('critique.all_rights')
def delete_latest_comment(req, slug):
    oeuvre = get_object_or_404(Oeuvre, slug=slug)
    n = len(oeuvre.comments)
    comments = sorted(enumerate(oeuvre.comments),
                      key=lambda p: p[1].date, reverse=True)
    del(oeuvre.comments[comments[0][0]])
    oeuvre.save()
    return redirect('detail_oeuvre', slug=slug)


# Top Textes

def top_textes(req):
    top_textes = TopTextes.objects.all()
    top_oeuvres = []
    for texte in top_textes:
        comment_idx = 0
        if hasattr(texte, 'comment_idx'):
            comment_idx = texte.comment_idx
        oeuvre = Oeuvre.objects.filter(id=texte.oeuvre_id)
        comment = oeuvre[0].comments[comment_idx]
        top_oeuvres.append((oeuvre[0], comment))
    top_oeuvres = sorted(top_oeuvres, key=lambda o: o[1].date, reverse=True)
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

def list_oeuvres(req, mtype="film", page=1):
    """
    Liste les oeuvres qui ne sont pas marquées en tant qu'envies.
    (Les "re-" envies ne sont pas prises en charge.)
    """
    oeuvres_list = Oeuvre.objects(__raw__={'envie': False, 'info.type': mtype})
    oeuvres = oeuvres_list.order_by('-info__year')
    context = {'oeuvres': oeuvres, 'mtype': mtype}
    return render(req, 'critique/collection.html', context)


# Envies

def list_envies(req, mtype="film", page=1):
    oeuvres_list = Oeuvre.objects(__raw__={'envie': True, 'info.type': mtype})
    oeuvres = oeuvres_list.order_by('-info__year')
    paginator = Paginator(oeuvres, 22)
    try:
        oeuvres_page = paginator.page(page)
    except EmptyPage:
        oeuvres_page = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres_page, 'mtype': mtype}
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
    """
    L'ordre des cinémas est aléatoire, mais constant pour un jour donné.
    """
    cinemas = list(Cinema.objects.all())
    random.seed(datetime.today().date())
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

@permission_required('critique.all_rights')
def update_seance(req, seance, data):
    seance.cinema = data['cinema']
    date = data['date']
    dtime = time(int(data['hour'][:2]), int(data['hour'][3:5]))
    seance.date = datetime.combine(date, dtime)
    if 'no_month' in data:
        seance.date_month_unknown = data['no_month']
    if ('film_slug' not in data and
        'seance_title' not in data):
        return
    if 'film_slug' in data and data['film_slug']:
        seance.film_id = str(get_object_or_404(Oeuvre, slug=data['film_slug']).id)
    elif 'seance_title' in data:
        seance.seance_title = data['seance_title']
    seance.save()

@permission_required('critique.all_rights')
def add_seance(req):
    form = SeanceForm(req.POST)
    seance = Seance()
    if form.is_valid():
        update_seance(req, seance, form.cleaned_data)
        return redirect('list_seances', year=seance.date.year)

def list_seances(req, year=2018):
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
    seances = Seance.objects(__raw__={'date': {'$gte': start, '$lte': end}}).order_by('date')

    seances_enhanced = []
    for seance in seances:
        film = None
        if seance.film_id:
            films = Oeuvre.objects.filter(id=seance.film_id)
            if len(films) > 0:      # and it should always be so
                film = films[0]
        seances_enhanced.append((seance, film))

    year_range = range(2012, 2019)
    return render(req, 'critique/seances.html', locals())


# Top Films

def top_films(req, year=2011):
    oeuvres_id = list(get_object_or_404(TopFilms, year=year).top)
    random.shuffle(oeuvres_id)
    oeuvres = []
    for oeuvre_id in oeuvres_id:
        oeuvres.append(Oeuvre.objects.filter(id=oeuvre_id)[0])
    year_range = range(2012, 2018)
    return render(req, 'critique/top_films.html', locals())
