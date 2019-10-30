#!/usr/bin/python

from pymongo import MongoClient
import random
import subprocess
import time

cli = MongoClient()
journal = cli.critique_bkp.oeuvre

res = journal.find({'info.type':'album'})

i = 0
for film in res:
    title_raw = film['info']['titles']['vf']
    if 'year' in film['info']:
        year = str(film['info']['year']) + '+'
    else:
        year = ''
    title = 'site:en.wikipedia.org+album+' + year + title_raw.replace("'", '').replace(' ', '+').replace('-', '').replace(':', '')
    subprocess.call(["scrapy runspider google_spider.py -t json --nolog -a search='%s' -o - > ttt.json" % title], shell=True)
    with open('ttt.json', 'a+') as f:
        s = f.read()
        idx = s.find(' "')
        idx2 = s.find('"', idx+2)
        if idx > 0 and idx2 > 0:
            wikipedia_id = s[idx+2:idx2]
            journal.find_one_and_update({'_id': film['_id']}, {'$set': {'info.imdb_id': wikipedia_id}})
            print i, title_raw, wikipedia_id
        else:
            print i, title_raw, 'XXXXX'
        i += 1
        time.sleep(random.random()*4)

