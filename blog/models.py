from django.contrib.auth.models import User
from django.db import models

from zinnia.models_bases.entry import AbstractEntry
from zinnia.models.entry import Entry


class EntryCustom(models.Model):
    entry = models.OneToOneField(Entry, related_name='custom',
                                 on_delete=models.CASCADE)
    lang = models.CharField('HTML lang', default="fr-FR", max_length=15)
    allowed_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.entry.title

    class Meta:
        verbose_name = u'Entry Custom'
        verbose_name_plural = u'Entries Custom'
