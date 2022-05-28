from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Cinema, Oeuvre


@receiver(post_delete, sender=Oeuvre)
def refresh_cache_collection_post_delete(sender, instance, *args, **kwargs):
    mtype = instance.mtype
    cache_key = make_template_fragment_key('chunks_collection', [mtype])
    cache.delete(cache_key)

"""
Receiver below does not work, partly because post_init catches
more OeuvreInfo creation than we want, and then loops...

from django.http import HttpRequest
from django.template.loader import render_to_string

@receiver(post_init, sender=OeuvreInfo)
def refresh_cache_post_init(sender, instance, *args, **kwargs):
    mtype = instance.mtype
    cache_key = make_template_fragment_key('chunks_collection', [mtype])
    cache.delete(cache_key)
    #oeuvres = Oeuvre.objects.filter(envie=False, info__mtype=mtype).order_by('-info__year', '-id')
    #context = {'mtype': mtype, 'oeuvres': oeuvres}
    #render_to_string('critique/collection.html', context=context)
    #
    #func, args, kwargs = resolve(reverse('list_oeuvres', args=[mtype]))
    #args = (HttpRequest(),) + args
    #func(*args, **kwargs)
"""

@receiver(post_save, sender=Cinema)
@receiver(post_delete, sender=Cinema)
def refresh_cache_cinemas(sender, instance, *args, **kwargs):
    cache_key = make_template_fragment_key('chunks_cinemas')
    cache.delete(cache_key)
