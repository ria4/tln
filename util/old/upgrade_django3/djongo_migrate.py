# db.critique_****.dropIndexes()

from bson.objectid import ObjectId
from pymongo import MongoClient

cli = MongoClient()


def migrate_oeuvre():
    oeuvre = cli.critique_django.oeuvre
    oeuvre_nu = cli.critique.critique_oeuvre

    oeuvres = oeuvre.find()

    o_nu = []
    for o in oeuvres:
        o["info"]["mtype"] = o["info"]["type"]
        del(o["info"]["type"])
        o_nu.append(o)

    r = oeuvre_nu.insert_many(o_nu)
    print("oeuvre", oeuvre.count_documents({}), len(r.inserted_ids))


def migrate_seance():
    seance = cli.critique_django.seance
    seance_nu = cli.critique.critique_seance

    seances = seance.find()

    o_nu = []
    for o in seances:
        if "film_id" in o:
            o["film_id"] = ObjectId(o["film_id"])
        o_nu.append(o)

    r = seance_nu.insert_many(o_nu)
    print("seance", seance.count_documents({}), len(r.inserted_ids))


def migrate_toptextes():
    toptextes = cli.critique_django.top_textes
    toptextes_nu = cli.critique.critique_toptextes

    toptextess = toptextes.find()

    o_nu = []
    for o in toptextess:
        o["oeuvre_id"] = ObjectId(o["oeuvre_id"])
        o_nu.append(o)

    r = toptextes_nu.insert_many(o_nu)
    print("toptextes", toptextes.count_documents({}), len(r.inserted_ids))


def migrate_topfilms():
    topfilms = cli.critique_django.top_films
    topfilms_nu = cli.critique.critique_topfilms

    topfilmss = topfilms.find()

    o_nu = []
    for o in topfilmss:
        o["top"] = [ObjectId(fid) for fid in o["top"]]
        o_nu.append(o)

    r = topfilms_nu.insert_many(o_nu)
    print("topfilms", topfilms.count_documents({}), len(r.inserted_ids))


def migrate_cinema():
    cinema = cli.critique_django.cinema
    cinema_nu = cli.critique.critique_cinema

    cinemas = cinema.find()

    o_nu = []
    for o in cinemas:
        o["comment"] = "\r\n\r\n".join(o["comment"])
        o_nu.append(o)

    r = cinema_nu.insert_many(o_nu)
    print("cinema", cinema.count_documents({}), len(r.inserted_ids))


migrate_oeuvre()
migrate_seance()
migrate_toptextes()
migrate_topfilms()
migrate_cinema()
