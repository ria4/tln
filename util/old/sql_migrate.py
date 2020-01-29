import pytz

from bson.objectid import ObjectId
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import timezone
from pymongo import MongoClient

from critique.models import *


cli = MongoClient()


def migrate_oeuvre():
    oeuvre = cli.critique_django.oeuvre
    oeuvres = oeuvre.find()

    toptextes = cli.critique_django.top_textes
    toptextess = toptextes.find()
    topcomments_oeuvres_id = [o["oeuvre_id"] for o in toptextess]

    i = 0
    for o in oeuvres:
        i += 1
        if not (i%100):
            print(i)

        vf = o["info"]["titles"]["vf"]
        vo = o["info"]["titles"].get("vo") or ""
        alt = ""
        if o["info"]["titles"].get("alt"):
            alt = o["info"]["titles"]["alt"][0]
        vinfotitres = Titres(vf=vf, vo=vo, alt=alt)
        vinfotitres.full_clean()
        vinfotitres.save()

        vartists = []
        for name in o["info"]["artists"]:
            slug = slugify(name)
            jaj = Artiste.objects.filter(slug=slug)
            if jaj and (jaj[0].name != name):
                raise Exception(name, jaj[0].name, slug)
            art, _ = Artiste.objects.get_or_create(name=name, slug=slug)
            vartists.append(art)

        mtype = o["info"]["type"]
        year = o["info"]["year"]
        imdb_id = o["info"].get("imdb_id") or ""
        image_url = o["info"].get("image_url") or ""
        vinfo = OeuvreInfo(mtype=mtype, titles=vinfotitres,
                           year=year, imdb_id=imdb_id, image_url=image_url)
        vinfo.full_clean()
        vinfo.save()
        vinfo.artists.set(vartists)

        envie = o["envie"]
        voeuvre = Oeuvre(info=vinfo, envie=envie, slug="0")
        # the actual slug is safely recomputed in __init__
        voeuvre.full_clean()
        voeuvre.save()

        if o.get("comments"):
            for comment in o["comments"]:
                title = comment.get("title") or ""
                date = timezone.make_aware(comment["date"], pytz.timezone(settings.TIME_ZONE))
                date_month_unknown = comment.get("date_month_unknown") or False
                date_day_unknown = comment.get("date_day_unknown") or False
                content = comment.get("content") or ""
                starred = str(o["_id"]) in topcomments_oeuvres_id
                vcomment = Commentaire(oeuvre=voeuvre,
                                       title=title, date=date,
                                       date_month_unknown=date_month_unknown,
                                       date_day_unknown=date_day_unknown,
                                       content=content, starred=starred)
                vcomment.full_clean()
                vcomment.save()

migrate_oeuvre()


def migrate_seance():
    seance = cli.critique_django.seance
    oeuvres = cli.critique_django.oeuvre
    seances = seance.find()

    for o in seances:
        cinema = o["cinema"] or "?"
        date = timezone.make_aware(o["date"], pytz.timezone(settings.TIME_ZONE))
        date_month_unknown = o.get("date_month_unknown") or False
        if o.get("film_id"):
            film = oeuvres.find_one({'_id': ObjectId(o["film_id"])})
            if film["slug"] == "dracula-2":
                film["slug"] = "dracula-1"
            elif film["slug"] == "faust-1":
                film["slug"] = "faust"
            elif film["slug"] == "faust-2":
                film["slug"] = "faust-1"
            elif film["slug"] == "le-vent-se-leve-2":
                film["slug"] = "le-vent-se-leve-1"
            elif film["slug"] == "week-end-1":
                film["slug"] = "week-end"
            elif film["slug"] == "week-end-2":
                film["slug"] = "week-end-1"
            elif film["slug"] == "batman-2":
                film["slug"] = "batman-1"
            elif film["slug"] == "mother-2":
                film["slug"] = "mother-1"
            elif film["slug"] == "high-life-2":
                film["slug"] = "high-life-1"
            elif film["slug"] == "tabou-1":
                film["slug"] = "tabou"
            f = Oeuvre.objects.get(slug=film["slug"])
            vseance = Seance(cinema=cinema, date=date, date_month_unknown=date_month_unknown,
                             film=f, seance_title="")
            vseance.full_clean()
            vseance.save()
        else:
            seance_title = o["seance_title"]
            vseance = Seance(cinema=cinema, date=date, date_month_unknown=date_month_unknown,
                             seance_title=seance_title)
            vseance.full_clean()
            vseance.save()

migrate_seance()


def migrate_topfilms():
    topfilms = cli.critique_django.top_films
    oeuvres = cli.critique_django.oeuvre
    topfilmss = topfilms.find()

    for o in topfilmss:
        vtop = []
        for fid in o["top"]:
            film = oeuvres.find_one({'_id': ObjectId(fid)})
            if film["slug"] == "dracula-2":
                film["slug"] = "dracula-1"
            elif film["slug"] == "faust-1":
                film["slug"] = "faust"
            elif film["slug"] == "faust-2":
                film["slug"] = "faust-1"
            elif film["slug"] == "le-vent-se-leve-2":
                film["slug"] = "le-vent-se-leve-1"
            elif film["slug"] == "week-end-1":
                film["slug"] = "week-end"
            elif film["slug"] == "week-end-2":
                film["slug"] = "week-end-1"
            elif film["slug"] == "batman-2":
                film["slug"] = "batman-1"
            elif film["slug"] == "mother-2":
                film["slug"] = "mother-1"
            elif film["slug"] == "high-life-2":
                film["slug"] = "high-life-1"
            elif film["slug"] == "tabou-1":
                film["slug"] = "tabou"
            f = Oeuvre.objects.get(slug=film["slug"])
            vtop.append(f)

        year = o["year"]
        vtopfilms = TopFilms(year=year)
        vtopfilms.save()
        vtopfilms.films.set(vtop)

migrate_topfilms()


def migrate_cinema():
    cinema = cli.critique_django.cinema
    cinemas = cinema.find()

    for o in cinemas:
        c = Cinema(name=o["name"],
                   slug=slugify(o["name"]),
                   comment="\r\n\r\n".join(o["comment"]),
                   visited=o["visited"])
        c.save()

migrate_cinema()
