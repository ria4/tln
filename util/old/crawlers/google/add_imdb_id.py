#!/usr/bin/python

from pymongo import MongoClient
import random
import subprocess
import time

cli = MongoClient()
journal = cli.critique.journal

#res = journal.find({'info.type':'film'})
#
#i = 0
#for film in res:
#    title_raw = film['info'][0]['title']
#    title = 'imdb+' + title_raw.replace("'", ' ').replace(' ', '+')
#    subprocess.call(["scrapy runspider imdb_spider.py -t json --nolog -a search='%s' -o - > ttt.json" % title], shell=True)
#    with open('ttt.json', 'a+') as f:
#        s = f.read()
#        idx = s.find(' "')
#        imdb_id = s[idx+2:idx+11]
#        journal.find_one_and_update({'info.title': title_raw}, {'$set': {'info.$.imdb_id': imdb_id}})
#        i += 1
#        print i, title_raw, imdb_id


res = journal.find({'info.type':'film'})

i = 0
for film in res[578:]:
    title_raw = film['info'][0]['title']
    title = 'imdb+' + title_raw.replace("'", ' ').replace(' ', '+').replace('-', ' ').replace(':', '')
    subprocess.call(["scrapy runspider google_spider.py -t json --nolog -a search='%s' -o - > ttt.json" % title], shell=True)
    with open('ttt.json', 'a+') as f:
        s = f.read()
        idx = s.find(' "')
        imdb_id = s[idx+2:idx+11]
        if imdb_id.startswith('tt'):
            journal.find_one_and_update({'info.title': title_raw}, {'$set': {'info.$.imdb_id': imdb_id}})
        i += 1
        print i, title_raw, imdb_id
        time.sleep(random.random()*3)

