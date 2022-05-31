from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, Paginator
from django.template.loader import render_to_string

from critique.models import Oeuvre, OeuvreTag


# Collection

def list_oeuvres_reqless(mtype):
    oeuvres = (
        Oeuvre.objects.filter(envie=False, mtype=mtype).order_by('-year', '-id')
    )
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
