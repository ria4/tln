from django.db import models

from zinnia.models_bases.entry import AbstractEntry


class EntryLang(AbstractEntry):
    lang = models.CharField('HTML lang', default="fr-FR", max_length=15)

    def __str__(self):
        return 'EntryLang %s' % self.title

    class Meta(AbstractEntry.Meta):
        abstract = True
