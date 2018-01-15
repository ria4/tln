
import os
import random
from datetime import datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Oeuvre, TopFilms, TopTextes, Cinema, Seance


def preambule(req):
    return render(req, 'critique/preambule.html', {})

def artiste(req, artist):
    oeuvres = Oeuvre.objects(__raw__={"$query": {'info.artists': artist}, "$orderby": {'info.year': 1}})
    context = {'oeuvres': oeuvres, 'artist': artist}
    return render(req, 'critique/artiste.html', context)

def detail_oeuvre(req, id):
    """
    Version qui extrait ou enregistre l'image dans un répertoire statique.
    L'image est stockée à la fois dans la base MongoDB et dans le répertoire,
    mais maintenant le client peut la mettre en cache...
    """
    oeuvre = get_object_or_404(Oeuvre, id=id)
    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre})

def detail_oeuvre_slug(req, slug):
    try:
        oeuvre = get_object_or_404(Oeuvre, slug=slug)
    except Oeuvre.MultipleObjectsReturned:
        oeuvres = Oeuvre.objects.filter(slug=slug)
        return render(req, 'critique/oeuvres.html', {'oeuvres': oeuvres})
    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre})

def liste_oeuvres(req, mtype, page=1):
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

def liste_envies(req, mtype, page=1):
    oeuvres_list = Oeuvre.objects(__raw__={'envie': True, 'info.type': mtype})
    paginator = Paginator(oeuvres_list, 22)
    try:
        oeuvres = paginator.page(page)
    except EmptyPage:
        oeuvres = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres, 'mtype': mtype}
    return render(req, 'critique/envies.html', context)

def liste_notes(req, mtype=None, page=1):
    if not mtype:
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

def top_films(req, year=2017):
    oeuvres = list(get_object_or_404(TopFilms, year=year).top)
    random.shuffle(oeuvres)
    year_range = range(2012, 2018)
    return render(req, 'critique/top_films.html', locals())

def top_textes(req):
    top_textes = get_object_or_404(TopTextes)
    top_oeuvres = []
    for texte in top_textes.textes:
        content = texte.content
        oeuvre = Oeuvre.objects(__raw__={'comments.content': content})
        top_oeuvres.append((oeuvre[0], texte))
    return render(req, 'critique/top_textes.html', locals())

def liste_cinemas(req, page=1):
    cinemas_list = Cinema.objects.all()
    paginator = Paginator(cinemas_list, 20)
    try:
        cinemas = paginator.page(page)
    except EmptyPage:
        cinemas = paginator.page(paginator.num_pages)
    return render(req, 'critique/cinemas.html', {'cinemas': cinemas})

def liste_seances(req, year=2017):
    if year > 2011:
        if year > 2017:
            year = 2017
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
    else:
        year = 2011
        start = datetime(2000, 1, 1)
        end = datetime(2011, 12, 31)
    seances = Seance.objects(__raw__={'date': {'$gte': start, '$lte': end}}).order_by('date')
    year_range = range(2012, 2018)
    return render(req, 'critique/seances.html', locals())



#import base64
#from tempfile import NamedTemporaryFile
#from shutil import copyfileobj

#def detail_oeuvre_tmpfile(req, slug):
#    """
#    Version qui crée un fichier temporaire.
#    """
#    try:
#        oeuvre = get_object_or_404(Oeuvre, slug=slug)
#        tmpFileObj = NamedTemporaryFile(dir='critique/static/critique')
#        copyfileobj(oeuvre.info.image, tmpFileObj)
#        tmpFileObj.seek(0, 0)
#        tmpFileObjName = 'critique/' + os.path.basename(tmpFileObj.name)
#    except Oeuvre.MultipleObjectsReturned:
#        raise Http404
#    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre, 'img_url': img_name})

#def detail_oeuvre_b64(req, slug):
#    """
#    Version qui transmet l'image en base64.
#    """
#    try:
#        oeuvre = get_object_or_404(Oeuvre, slug=slug)
#        img = oeuvre.info.image.read()
#        img_b64 = base64.encodebytes(img).decode('utf-8')
#    except Oeuvre.MultipleObjectsReturned:
#        raise Http404
#    return render(req, 'critique/oeuvre.html', {'oeuvre': oeuvre, 'img_b64': img_b64})

