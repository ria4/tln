from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from critique.models import Cinema, Oeuvre


# @receiver(post_init, sender=Oeuvre)  # does not work because of loops?
@receiver(post_delete, sender=Oeuvre)
def refresh_cache_collection(sender, instance, *args, **kwargs):
    cache_key = make_template_fragment_key('chunks_collection', [instance.mtype])
    cache.delete(cache_key)


@receiver(post_save, sender=Cinema)
@receiver(post_delete, sender=Cinema)
def clear_cache_cinemas(sender, instance, *args, **kwargs):
    cache_key = make_template_fragment_key('chunks_cinemas')
    cache.delete(cache_key)
