
import mongoengine, sys
from datetime import datetime
from pymongo import MongoClient
from blog.models import *


def save(i, item):
    info = item["info"][0]

    titres = OeuvreInfoTitres()
    titres_vf = info["titles"][0]["vf"]
    while titres_vf[-1] in [" ", "\xa0"]:
        titres_vf = titres_vf[:-1]
    titres.vf = titres_vf
    print(i, titres.vf)
    if len(info["titles"]) > 1:
        vo = info["titles"][1]["vo"]
        if vo:
            titres.vo = vo

    oinfo = OeuvreInfo()
    oinfo.type = info["type"]
    oinfo.titles = titres
    if "artists" in info:
        artists = info["artists"]
        if isinstance(artists[0], str):
            oinfo.artists = artists
        else:
            oinfo.artists = [artists[0]["artist"]]
    if "year" in info:
        year = info["year"]
        if len(year) != 4:
            year = year[-4:]
        try:
            y = int(year)
            oinfo.year = y
        except ValueError:
            pass
    if "imdb_id" in info and info["imdb_id"]:
        oinfo.imdb_id = info["imdb_id"]
    if ("image" in info) and info["image"][0] == "M":
        oinfo.image = "media/illustrations_oeuvres/%s" % info["image"]

    if len(item["comment"]) == 0:
        ocomment = None
    else:
        comment = item["comment"][0]
        ocomment = OeuvreComment()
        if "title" in comment:
            ocomment.title = comment["title"]
        date = comment["date"]
        if len(date) == 8:
            ocomment.date = datetime.strptime(date, '%y-%m-%d')
        elif len(date) == 5:
            ocomment.date = datetime.strptime(date+'-01', '%y-%m-%d')
            ocomment.date_day_unknown = True
        elif len(date) == 2:
            ocomment.date = datetime.strptime(date+'-01-01', '%y-%m-%d')
            ocomment.date_day_unknown = True
            ocomment.date_month_unknown = True
        else:
            raise Exception('unknown date format')
        ocomment.content = [a["par"] for a in comment["content"]]

    o = Oeuvre()
    o.info = oinfo
    o.envie = len(item["tags"]) > 0
    if ocomment:
        o.comments = [ocomment]

    o.save()


cli = MongoClient()
journal = cli.critique.journal
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

