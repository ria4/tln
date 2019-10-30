#!/usr/bin/python
#encoding: utf-8

from pymongo import MongoClient

cli = MongoClient()
journal = cli.critique.journal

res = journal.find()

for item in res:
    info = item['info'][0]
    if 'artist' in info:
        artist = info['artist']
        journal.update_one({'_id': item['_id']}, {"$unset": {"info.0.artist": ""}})
        journal.update_one({'_id': item['_id']}, {"$set": {"info.0.artists": [{'artist': artist}]}})

