
import locale
import mongoengine, sys
from datetime import datetime
from pymongo import MongoClient
from critique.models import *


locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

def save(i, item):
    year = item["year"]
    seances = item["seances"]

    for s in seances:
        seance = Seance()
        seance.cinema = s["cinema"]
        seance.film = s["film"]

        if not s["date"]:
            seance.date = datetime(int(year), 1, 1)
            seance.date_day_unknown = True
        elif s["date"] == "8 décembre, 20h31 bis":
            seance.date = datetime(int(year), 12, 8, 20, 31)
        else:
            try:
                seance.date = datetime.strptime(s["date"], '%d %B %Y, %Hh%M')
            except Exception:
                try:
                    seance.date = datetime.strptime(s["date"], '%d %B %Y, %Hh')
                except Exception:
                    try:
                        seance.date = datetime.strptime(year + ' ' + s["date"],
                                                        '%Y %d/%m, %Hh%M')
                    except Exception:
                        try:
                            seance.date = datetime.strptime(year + ' ' + s["date"],
                                                            '%Y %d/%m, %Hh')
                        except Exception:
                            try:
                                seance.date = datetime.strptime(year + ' ' + s["date"],
                                                                '%Y %d %B, %Hh%M')
                            except Exception:
                                seance.date = datetime.strptime(year + ' ' + s["date"],
                                                                '%Y %d %B, %Hh')

        print(seance.cinema, seance.film, seance.date)
        seance.save()


cli = MongoClient()
journal = cli.critique.seances
res = journal.find()

mongoengine.connect('critique_django', alias='default')

for i, item in enumerate(res):
    try:
        save(i, item)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

