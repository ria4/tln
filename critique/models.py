import os

from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


OEUVRES_TYPES = [
    ('film', 'Film'),
    ('serie', 'Série'),
    ('album', 'Album'),
    ('jeu', 'Jeu'),
    ('livre', 'Livre'),
    ('bd', 'BD'),
]


class RightsSupport(models.Model):
    """
    This is a dummy Model for managing permissions without them
    being linked to a particular Model.
    """
    class Meta:
        managed = False
        permissions = (('all_rights', 'All rights'),)


def create_image_url(image):
    img_url = 'critique/' + image.md5
    img_path = 'critique/static/' + img_url
    if not os.path.isfile(img_path):
        with open(img_path, 'wb') as f:
            f.write(image.read())
    return img_url


class OeuvreInfoTitres(models.Model):
    """
    Titres possibles de l'oeuvre.
    Dans le cas d'un titre non traduit (e.g. pour les albums...)
    ou d'une production française, 'vf' est rempli mais 'vo' est laissé vide.
    L'attribut 'alt' peut être utilisé pour contenir un autre titre.
    """
    vf = models.CharField(max_length=200)
    vo = models.CharField(max_length=200, blank=True)
    alt = models.CharField(max_length=200, blank=True)

class OeuvreArtist(models.Model):
    name = models.CharField(max_length=100)

class OeuvreInfo(models.Model):
    """
    Informations publiques sur l'oeuvre.
    L'attribut imdb_id ne devrait pas apparaître en dehors du type 'film'.
    """
    mtype = models.CharField(max_length=5, choices=OEUVRES_TYPES)
    titles = models.OneToOneField(OeuvreInfoTitres, on_delete=models.CASCADE)
    artists = models.ManyToManyField(OeuvreArtist)
    year = models.SmallIntegerField()
    imdb_id = models.CharField(max_length=10, blank=True)
    image_url = models.CharField(max_length=45, blank=True)
    # use Validator for regexes '^tt[0-9]{7,8}$' & '^critique/[a-f0-9]{32}.jpg'

class OeuvreComment(models.Model):
    """
    Commentaire personnel sur l'oeuvre, avec titre optionnel.
    Certaines dates ont été importées avec le jour ou le mois fixé à 01.
    Elles sont identifiées par date_{day|month}_unknown à True.
    """
    title = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=timezone.now)
    date_month_unknown = models.BooleanField(default=False)
    date_day_unknown = models.BooleanField(default=False)
    content = models.TextField(blank=True)

class OeuvreTag(models.Model):
    tag = models.CharField(max_length=100)

class Oeuvre(models.Model):
    """
    Modèle pour une oeuvre.
    """
    info = models.OneToOneField(OeuvreInfo, on_delete=models.CASCADE)
    tags = models.ManyToManyField(OeuvreTag, blank=True)
    envie = models.BooleanField(default=False)
    comments = models.ManyToManyField(OeuvreComment, blank=True)
    slug = models.CharField(max_length=200, unique=True)

    def __init__(self, *args, **kwargs):
        super(Oeuvre, self).__init__(*args, **kwargs)
        if "info" not in kwargs:
            self.info = OeuvreInfo()
            self.info.titles = OeuvreInfoTitres()

    @classmethod
    def get_safe_slug(cls, slug_base, updating=False):
        """
        Retourne un slug unique, en fonction des slugs existants.
        /!\ La suppression d'une oeuvre ne modifiera pas les homonymes.
        """
        oeuvres = cls.objects.filter(slug=slug_base)
        if len(oeuvres) == 0:
            slug_1 = "%s-1" % slug_base
            oeuvres = cls.objects.filter(slug=slug_1)
            if len(oeuvres) == 0:
                return slug_base
            elif len(oeuvres) == 1:
                i = 2
                slug = "%s-%d" % (slug_base, i)
                while cls.objects.filter(slug=slug):
                    i += 1
                    slug = "%s-%d" % (slug_base, i)
                return slug
        elif len(oeuvres) == 1:
            if updating:
                return slug_base
            else:
                oeuvres[0].slug = "%s-1" % slug_base
                oeuvres[0].save()
                return "%s-2" % slug_base

    def save(self, *args, **kwargs):
        cls = self.__class__
        if not self.id:
            self.slug = cls.get_safe_slug(slugify(self.info.titles.vf))
        elif self.info.titles.vf != cls.objects.filter(id=self.id)[0].info.titles.vf:
            self.slug = cls.get_safe_slug(slugify(self.info.titles.vf), updating=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.info.titles.vf


class TopFilms(models.Model):
    year = models.SmallIntegerField(unique=True)
    top = models.ManyToManyField(Oeuvre)

class TopTextes(models.Model):
    oeuvre_id = models.ForeignKey(Oeuvre, on_delete=models.CASCADE)
    comment_idx = models.SmallIntegerField(blank=True, null=True)

class Cinema(models.Model):
    name = models.CharField(max_length=100, unique=True)
    comment = models.TextField()
    visited = models.DateField()

class Seance(models.Model):
    """
    Renseigner un film_id suffit pour la plupart des cas, mais pour des séances
    spéciales, sans oeuvre correspondante, il est possible de donner un titre.
    """
    cinema = models.CharField(max_length=100)
    date = models.DateTimeField()
    date_month_unknown = models.BooleanField(default=False)
    film_id = models.ForeignKey(Oeuvre, on_delete=models.SET_NULL, blank=True, null=True)
    seance_title = models.CharField(max_length=200, blank=True)
