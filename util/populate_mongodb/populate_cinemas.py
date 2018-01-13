
import locale
import mongoengine, sys
from datetime import datetime
from pymongo import MongoClient
from critique.models import *


locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

def clean_comment(s):
    res = []
    while s.find('\n') > 0:
        idx = s.find('\n')
        res.append(s[:idx])
        s = s[idx+1:]
        while s[:1] == '\n':
            s = s[1:]
    res.append(s)
    return res

def save(i, item):
    cinema = Cinema()

    cinema.name = item["cinema"]

    try:
        cinema.visited = datetime.strptime(item["visited"], '%d %B %Y')
    except Exception:
        cinema.visited = datetime(1901, 1, 1)

    cinema.comment = clean_comment(item["comment"])

    cinema.save()


cli = MongoClient()
journal = cli.critique.cinemas_parisiens
res = journal.find()

mongoengine.connect('critique_django', alias='default')

for i, item in enumerate(res):
    try:
        if "cinema" in item:
            save(i, item)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

