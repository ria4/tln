import threading

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import get_object_or_404, redirect, render
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

    # redirects for top jeux
    if slug == "top_jeux":
        return redirect("top_jeux")

    # redirects for tops ciné
    if slug == "top_cine":
        return redirect("top_films")
    elif slug.startswith("top_cine_"):
        return redirect("top_films", year=slug[-4:])

    tag = get_object_or_404(OeuvreTag, slug=slug)
    oeuvres_list = Oeuvre.objects.filter(tags=tag)
    oeuvres = oeuvres_list.order_by('-year', '-id')
    paginator = Paginator(oeuvres, 22)
    try:
        oeuvres_page = paginator.page(page)
    except EmptyPage:
        oeuvres_page = paginator.page(paginator.num_pages)
    context = {'oeuvres': oeuvres_page, 'tag': tag}
    return render(req, 'critique/tag.html', context)


# Oeuvre Cache

def refresh_oeuvre_cache(mtype):
    """Refresh the template fragment cached for the mtype collection.

    Note that we use template fragment caching instead of per-view caching
    because Django does not provide a proper way to clear per-view caches.
    """
    # release the template fragment cache key
    cache_key = make_template_fragment_key('chunks_collection', [mtype])
    cache.delete(cache_key)
    # get the current oeuvres
    context = list_oeuvres_reqless(mtype)
    # generate the oeuvres template, and update the cache accordingly
    render_to_string('critique/collection.html', context=context)

def refresh_oeuvre_cache_threaded(mtype):
    """Refresh the oeuvre cache in a new thread, to avoid time overhead.

    The target function does not need to close django's database connection,
    as long as CONN_MAX_AGE remains the default 0 (meaning that connections are
    opened and closed automatically upon each request).
    See https://docs.djangoproject.com/en/5.0/ref/databases/#persistent-connections

    Note that the thread will exit on its own, once the target function returns.
    """
    t = threading.Thread(
        target=refresh_oeuvre_cache,
        args=[mtype],
        daemon=True,
    )
    t.start()
