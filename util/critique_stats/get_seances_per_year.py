#!/usr/bin/python

"""
# vtln
(tln)$ python util/critique_stats/get_seances_stats.py

Print number of seances per year & number of seances per cinema.
"""

from collections import OrderedDict
import os
import pprint
import sys

import django
from django.db.models import Count, F
from django.db.models.functions import TruncYear

sys.path.append('/home/ria/tln')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tln.settings')
django.setup()

from critique.models import Seance


stats = (
    Seance.objects.annotate(year=TruncYear("oeuvre_span__date_start"))
    .values("year")
    .annotate(cnt=Count("id"))
)
stats = {stat["year"].year: stat["cnt"] for stat in stats}
print("### Number of seances per year ###")
pprint.pprint(stats)
print()

stats = (
    Seance.objects.annotate(cinema_name=F("cinema__name"))
    .values("cinema_name")
    .annotate(cnt=Count("id"))
    .order_by("-cnt")
)
stats = OrderedDict([(stat["cinema_name"], stat["cnt"]) for stat in stats])
stats_cleaned = OrderedDict()
side_cnt = 0
for cinema, cnt in stats.items():
    if cnt <= 15:
        side_cnt += cnt
    else:
        stats_cleaned[cinema] = cnt
stats_cleaned["others <= 15"] = side_cnt
print("### Number of seances per cinema ###")
pprint.pprint(stats_cleaned)
