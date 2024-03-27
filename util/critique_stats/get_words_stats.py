#!/usr/bin/python

"""
# vtln
(tln)$ python util/critique_stats/get_words_stats.py

Print number of characters written per year, absolute & relative to number of texts.
"""

from collections import OrderedDict
import os
import pprint
import sys

import django
from django.db.models import Count, Sum
from django.db.models.functions import Length, TruncYear

sys.path.append('/home/ria/tln')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tln.settings')
django.setup()

from critique.models import Commentaire


stats = (
    Commentaire.objects.values(year=TruncYear("date"))
    .annotate(cnt_chars=Sum(Length("content")), cnt_texts=Count("id"))
)
stats = {
    stat["year"].year: (
        stat["cnt_texts"],
        stat["cnt_chars"],
        int(stat["cnt_chars"] / stat["cnt_texts"]),
    ) for stat in stats
}
print("### Number of chars written per year (#texts, #chars, ratio) ###")
pprint.pprint(stats)
