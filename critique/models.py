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


class Titres(models.Model):
    """
    Titres possibles d'une oeuvre.
    Dans le cas d'un titre non traduit (e.g. pour les albums...)
    ou d'une production française, 'vf' est rempli mais 'vo' est laissé vide.
    L'attribut 'alt' peut être utilisé pour contenir un autre titre.
    """
    vf = models.CharField(max_length=200, db_index=True)
    vo = models.CharField(max_length=200, blank=True, db_index=True)
    alt = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.vf


class Artiste(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class OeuvreInfo(models.Model):
    """
    Informations publiques sur l'oeuvre.
    L'attribut imdb_id ne devrait pas apparaître en dehors du type 'film'.
    """
    mtype = models.CharField(max_length=5, choices=OEUVRES_TYPES)
    titles = models.OneToOneField(Titres, on_delete=models.CASCADE,
                                  related_name="oeuvre_info",
                                  related_query_name="oeuvre_info")
    artists = models.ManyToManyField(Artiste,
                                     related_name="oeuvres_info",
                                     related_query_name="oeuvre_info")
    year = models.SmallIntegerField(db_index=True)
    imdb_id = models.CharField(max_length=10, blank=True)
    image_url = models.CharField(max_length=45, blank=True)
    # use Validator for regexes '^tt[0-9]{7,8}$' & '^critique/[a-f0-9]{32}.(jpg|png)'

    def __str__(self):
        return str(self.titles)


class OeuvreTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, update_slug=False, *args, **kwargs):
        if ((not self.id) or update_slug):
            # si création ou bien modification du nom, création d'un slug
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Oeuvre(models.Model):
    """
    Modèle pour une oeuvre.
    """
    info = models.OneToOneField(OeuvreInfo, on_delete=models.CASCADE,
                                related_name="oeuvre",
                                related_query_name="oeuvre")
    tags = models.ManyToManyField(OeuvreTag, blank=True,
                                  related_name="oeuvres",
                                  related_query_name="oeuvre")
    envie = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    @classmethod
    def get_safe_slug(cls, slug_base):
        """
        Retourne un slug unique, en fonction des slugs existants.
        Pour les homonymes, on a dans l'ordre : oeuvre, oeuvre-1, oeuvre-2...
        /!\ La suppression d'une oeuvre ne modifiera pas les homonymes.
        """
        slug_base = slug_base or "dummyslug"
        oeuvres = Oeuvre.objects.filter(slug=slug_base)
        if len(oeuvres) == 0:
            return slug_base
        else:
            i = 1
            slug = "%s-%d" % (slug_base, i)
            while Oeuvre.objects.filter(slug=slug):
                i += 1
                slug = "%s-%d" % (slug_base, i)
            return slug

    def save(self, update_slug=False, *args, **kwargs):
        cls = self.__class__
        if ((not self.id) or update_slug):
            # si création ou bien modification du titre vf, création d'un slug
            self.slug = cls.get_safe_slug(slugify(self.info.titles.vf))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.info)


class Commentaire(models.Model):
    """
    Commentaire personnel sur l'oeuvre, avec titre optionnel.
    Certaines dates ont été importées avec le jour ou le mois fixé à 01.
    Elles sont identifiées par date_{day|month}_unknown à True.
    """
    oeuvre = models.ForeignKey(Oeuvre, on_delete=models.CASCADE,
                               related_name="comments",
                               related_query_name="comment")
    title = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=timezone.now)
    date_month_unknown = models.BooleanField(default=False)
    date_day_unknown = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    starred = models.BooleanField(default=False)

    def __str__(self):
        return f'"{self.content:.60}..." [{self.oeuvre}, {self.date.date()}]'


class TopFilms(models.Model):
    year = models.SmallIntegerField(unique=True)
    films = models.ManyToManyField(Oeuvre,
                                   related_name="top_films",
                                   related_query_name="top_films")

    def __str__(self):
        return str(self.year)


class TopJeux(models.Model):
    year = models.SmallIntegerField(unique=True)
    jeux = models.ManyToManyField(Oeuvre,
                                  related_name="top_jeux",
                                  related_query_name="top_jeux")

    def __str__(self):
        return str(self.year)


class Cinema(models.Model):
    """The names do not need to be unique, but we should reuse get_safe_slug then."""
    name = models.CharField(max_length=100, unique=True)
    name_short = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name_long = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    comment = models.TextField(blank=True)
    visited = models.DateField(blank=True, null=True)

    def save(self, update_slug=False, *args, **kwargs):
        if ((not self.id) or update_slug):
            # si création ou bien modification du nom, création d'un slug
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Seance(models.Model):
    """
    Renseigner un film_id suffit pour la plupart des cas, mais pour des séances
    spéciales, sans oeuvre correspondante, il est possible de donner un titre.
    """
    cinema = models.ForeignKey(Cinema, on_delete=models.PROTECT,
                               null=True, related_name="seances",
                               related_query_name="seance")
    cinema_name_short_override = models.CharField(max_length=100, blank=True)
    cinema_name_long_override = models.CharField(max_length=100, blank=True)
    cinema_unsure = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True)
    date_month_unknown = models.BooleanField(default=False)
    date_day_unknown = models.BooleanField(default=False)
    film = models.ForeignKey(Oeuvre, on_delete=models.SET_NULL,
                             blank=True, null=True,
                             related_name="seances",
                             related_query_name="seance")
    seance_title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        title = str(self.film) or self.seance_title
        cinema_name = None
        if self.cinema:
            cinema_name = self.cinema.name_short or self.cinema.name
        return f"{cinema_name} | {self.date.date()} | {title}"
