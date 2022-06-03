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


class Artiste(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


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

    L'attribut imdb_id ne devrait pas apparaître en dehors du type 'film'.

    Dans le cas d'un titre non traduit (e.g. pour les albums...)
    ou d'une production française, 'vf' est rempli mais 'vo' est laissé vide.
    L'attribut 'alt' peut être utilisé pour contenir un autre titre.
    """
    mtype = models.CharField(max_length=5, choices=OEUVRES_TYPES)
    title_vf = models.CharField(max_length=200, db_index=True)
    title_vo = models.CharField(max_length=200, blank=True, db_index=True)
    title_alt = models.CharField(max_length=200, blank=True)
    year = models.SmallIntegerField(db_index=True)
    imdb_id = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='oeuvres_img', blank=True)
    envie = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    artists = models.ManyToManyField(
        Artiste,
        related_name="oeuvres",
        related_query_name="oeuvre",
    )
    tags = models.ManyToManyField(
        OeuvreTag,
        blank=True,
        related_name="oeuvres",
        related_query_name="oeuvre",
    )

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
            self.slug = cls.get_safe_slug(slugify(self.title_vf))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_vf


class OeuvreSpan(models.Model):
    """Intervalle de temps à associer à une œuvre.

    Pour les séances avec titre mais sans film, oeuvre vaut None."""

    oeuvre = models.ForeignKey(
        Oeuvre,
        db_index=True,
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="spans",
        related_query_name="span",
    )
    date_start = models.DateTimeField()
    date_start_du = models.BooleanField(default=False)
    date_start_mu = models.BooleanField(default=False)
    date_end = models.DateTimeField()
    date_end_du = models.BooleanField(default=False, blank=True)
    date_end_mu = models.BooleanField(default=False, blank=True)
    ongoing = models.BooleanField(default=False, blank=True)

    def __str__(self):
        o = str(self.oeuvre)
        ds = self.date_start.date()
        de = None
        if self.date_end:
            de = self.date_end.date()
        return f"{o} | {ds} | {de}"


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
    date_du = models.BooleanField(default=False)
    date_mu = models.BooleanField(default=False)
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
    oeuvre_span = models.OneToOneField(
        OeuvreSpan,
        on_delete=models.CASCADE,
    )
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.PROTECT,
        null=True,
        related_name="seances",
        related_query_name="seance",
    )
    cinema_name_short_override = models.CharField(max_length=100, blank=True)
    cinema_name_long_override = models.CharField(max_length=100, blank=True)
    cinema_unsure = models.BooleanField(default=False)
    seance_title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        title = self.seance_title or str(self.oeuvre_span.oeuvre)
        date_seance = self.oeuvre_span.date_start.date()
        cinema_name = None
        if self.cinema:
            cinema_name = self.cinema.name_short or self.cinema.name
        return f"{cinema_name} | {date_seance} | {title}"
