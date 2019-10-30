#!/usr/bin/python
#encoding: utf-8

from pymongo import MongoClient

cli = MongoClient()
journal = cli.critique.journal

res = journal.find()

for item in res:
    info = item['info'][0]
    if 'title' in info:
        title = info['title']
        journal.update_one({'_id': item['_id']}, {"$unset": {"info.0.title": ""}})
        journal.update_one({'_id': item['_id']}, {"$set": {"info.0.titles": [{'vf': title}]}})

