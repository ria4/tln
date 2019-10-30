
from pymongo import MongoClient


def save(i, iem):
    for n, item in enumerate(iem["top"]):
        if "image_url" in item["info"] and item["info"]["image_url"]:
            journal.update({'_id': iem['_id']}, {'$set': {'top.'+str(n)+'.info.image_url': item["info"]["image_url"] + ".jpg"}})


cli = MongoClient()
journal = cli.critique_django.top_films
res = journal.find()

for i, item in enumerate(res):
    try:
        save(i, item)
    except Exception as e:
        print(item)
        print()
        print(e)
        sys.exit()

