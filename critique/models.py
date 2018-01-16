
import os
from datetime import datetime
from django.template.defaultfilters import slugify
from django_mongoengine import Document, EmbeddedDocument, fields

OEUVRES_TYPES = ('film', 'serie', 'album', 'jeu', 'livre', 'bd')


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
    image = fields.ImageField(upload_to='illustrations_oeuvres/', blank=True)
    image_url = fields.StringField(regex='^critique/[a-f0-9]{32}$', blank=True)

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
    Actuellement, le slug enregistré n'est pas forcément unique !
    """
    info = fields.EmbeddedDocumentField(OeuvreInfo)
    tags = fields.ListField(fields.StringField(max_length=100), blank=True, null=True)
    envie = fields.BooleanField(default=False)
    comments = fields.ListField(fields.EmbeddedDocumentField(OeuvreComment), blank=True, null=True)
    slug = fields.StringField()

    def save(self, *args, **kwargs):
        """
        Un slug est généré à la création et à chaque modification.
        Par défaut, l'image est dupliquée et enregistrée dans static/critique/.
        Cela vise à permettre la mise en cache d'images par les clients.
        """
        self.slug = slugify(self.info.titles.vf)
        #if self.info.image.md5 and not self.info.image_url:
        #    self.info.image_url = create_image_url(self.info.image)
        super(Oeuvre, self).save(*args, **kwargs)

    def __str__(self):
        return self.info.titles.vf


class TopFilms(Document):
    year = fields.IntField(max_value=2100, unique=True)
    top = fields.ListField(fields.EmbeddedDocumentField('Oeuvre'))

class TopTextes(Document):
    """
    There should only be one document in the associatied collection.
    """
    textes = fields.ListField(fields.EmbeddedDocumentField('OeuvreComment'))

class Cinema(Document):
    name = fields.StringField(max_length=100)
    comment = fields.ListField(fields.StringField())
    visited = fields.DateTimeField()

class Seance(Document):
    cinema = fields.StringField(max_length=100)
    date = fields.DateTimeField()
    date_day_unknown = fields.BooleanField(default=False)
    film = fields.StringField(max_length=500)
