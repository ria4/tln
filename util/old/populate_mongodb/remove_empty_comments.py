
import sys
from pymongo import MongoClient


cli = MongoClient()
journal = cli.critique_django.oeuvre
res = journal.find({'comments.0.content':[""]})

for i, item in enumerate(res):
    try:
        vf = item["info"]["titles"]["vf"]
        journal.update_one({"_id": item["_id"]}, {"$unset": {"comments": ""}})
        print(i, vf)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

