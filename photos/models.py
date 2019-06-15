from django.contrib.auth.models import User
from django.db import models

from photologue.models import Gallery


class GalleryCustom(models.Model):
    gallery = models.OneToOneField(Gallery, related_name='custom',
                                   on_delete=models.CASCADE)
    date_shooting = models.CharField('Date du projet', max_length=31)
    description_fr = models.TextField('Description FR', blank=True)
    description_en = models.TextField('Description EN', blank=True)
    allowed_users = models.ManyToManyField(User)

    class Meta:
        verbose_name = u'Gallery Custom'
        verbose_name_plural = u'Galleries Custom'

    def __str__(self):
        return self.gallery.title
