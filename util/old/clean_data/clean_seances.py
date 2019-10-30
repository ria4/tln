
import sys
from pymongo import MongoClient


cli = MongoClient()
journal = cli.critique_django.seance
res = journal.find({})

for i, item in enumerate(res):
    try:
        journal.update_one({"_id": item["_id"]}, {"$unset": {"film": 0}})
        journal.update_one({"_id": item["_id"]}, {"$unset": {"date_day_unknown": 0}})
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

