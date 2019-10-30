
import sys
from pymongo import MongoClient
from django.template.defaultfilters import slugify


cli = MongoClient()
journal = cli.critique_django.oeuvre
res = journal.find()

for i, item in enumerate(res):
    try:
        vf = item["info"]["titles"]["vf"]
        slug = slugify(vf)
        journal.update_one({"_id": item["_id"]}, {"$set": {"slug": slug}})
        print(i, vf)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

