OEUVRE_MTYPES = [
    ('film', 'Film'),
    ('serie', 'Série'),
    ('album', 'Album'),
    ('jeu', 'Jeu'),
    ('livre', 'Livre'),
    ('bd', 'BD'),
]

MTYPE_ATTRIBUTION_MAP = {
    "film": ("un film réalisé par"),
    "serie": ("une série supervisée par"),
    "album": ("un album de"),
    "jeu": ("un jeu développé par"),
    "livre": ("un livre écrit par"),
    "bd": ("une BD de"),
}

# second element of the tuple indicates un accord féminin
MTYPE_SPAN_MAP = {
    'film': ('vu ', False),
    'serie': ('regardée ', True),
    'album': ('écouté ', False),
    'jeu': ('joué ', False),
    'livre': ('lu ', False),
    'bd': ('lue ', True),
}

CINEMA_LONGNAME_PREFIXES = [
    'au cinéma ',
    'au centre ',
    'au ',
    'aux ',
    'à la ',
    'à l\'',
    'dans ',
]

OEUVRES_IMG_TMP_DIR = '/tmp/oeuvres_img'

MAX_SPANS_ON_OEUVRE = 3
