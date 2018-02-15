import os
from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django_mongoengine import Document, EmbeddedDocument, fields

OEUVRES_TYPES = ('film', 'serie', 'album', 'jeu', 'livre', 'bd')


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


class OeuvreInfoTitres(EmbeddedDocument):
    """
    Titres possibles de l'oeuvre.
    Dans le cas d'un titre non traduit (e.g. pour les albums...)
    ou d'une production française, 'vf' est rempli mais 'vo' est laissé vide.
    L'attribut 'alt' peut être utilisé pour contenir d'autres titres.
    """
    vf = fields.StringField(max_length=1000)
    vo = fields.StringField(max_length=1000, blank=True)
    alt = fields.ListField(fields.StringField(max_length=1000), blank=True, null=True)

class OeuvreInfo(EmbeddedDocument):
    """
    Informations publiques sur l'oeuvre.
    L'attribut imdb_id ne devrait pas apparaître en dehors du type 'film'.
    TODO: make artists & year mandatory once the db has been properly filled
    """
    type = fields.StringField(choices=OEUVRES_TYPES)
    titles = fields.EmbeddedDocumentField(OeuvreInfoTitres)
    #artists = fields.ListField(fields.StringField(max_length=100))
    #year = fields.IntField(max_value=2100)
    artists = fields.ListField(fields.StringField(max_length=100), blank=True)
    year = fields.IntField(max_value=2100, blank=True)
    imdb_id = fields.StringField(regex='^tt[0-9]{7}$', blank=True, null=True)
    image_url = fields.StringField(regex='^critique/[a-f0-9]{32}.jpg', blank=True)

class OeuvreComment(EmbeddedDocument):
    """
    Commentaire personnel sur l'oeuvre, avec titre optionnel.
    Certaines dates ont été importées avec le jour ou le mois fixé à 01.
    Elles sont identifiées par date_{day|month}_unknown à True.
    """
    title = fields.StringField(max_length=500, blank=True)
    date = fields.DateTimeField(default=datetime.now())
    date_month_unknown = fields.BooleanField(default=False)
    date_day_unknown = fields.BooleanField(default=False)
    content = fields.ListField(fields.StringField(), blank=True)

class Oeuvre(Document):
    """
    Modèle pour une oeuvre.
    """
    info = fields.EmbeddedDocumentField(OeuvreInfo)
    tags = fields.ListField(fields.StringField(max_length=100), blank=True, null=True)
    envie = fields.BooleanField(default=False)
    comments = fields.ListField(fields.EmbeddedDocumentField(OeuvreComment), blank=True, null=True)
    slug = fields.StringField(unique=True)

    def __init__(self, *args, **kwargs):
        super(Oeuvre, self).__init__(*args, **kwargs)
        if "info" not in kwargs:
            self.info = OeuvreInfo()
            self.info.titles = OeuvreInfoTitres()

    @classmethod
    def get_safe_slug(cls, slug_base, updating=False):
        """
        Retourne un slug unique, en fonction des slugs existants.
        Cela peut passer par la mise à jour d'un autre slug.
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


class TopFilms(Document):
    year = fields.IntField(max_value=2100, unique=True)
    top = fields.ListField(fields.StringField(max_length=24))

class TopTextes(Document):
    oeuvre_id = fields.StringField(max_length=24)
    comment_idx = fields.IntField(default=0)

class Cinema(Document):
    name = fields.StringField(max_length=100)
    comment = fields.ListField(fields.StringField())
    visited = fields.DateTimeField()

class Seance(Document):
    cinema = fields.StringField(max_length=100)
    date = fields.DateTimeField()
    date_day_unknown = fields.BooleanField(default=False)
    film = fields.StringField(max_length=500)
