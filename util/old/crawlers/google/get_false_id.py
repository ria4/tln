#!/usr/bin/python

from pymongo import MongoClient

cli = MongoClient()
journal = cli.critique.journal

res = journal.find({ '$or': [{'info.type':'film'}, {'info.type':'serie'}]})

for item in res:
    info = item['info'][0]
    if not 'imdb_id' in info:
        print info['title']
    elif not info['imdb_id'].startswith('tt'):
        print info['title'], info['imdb_id']

