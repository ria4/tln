#!/usr/bin/python
# coding: utf-8

import codecs, json, os, random, subprocess, time, urllib

from pymongo import MongoClient


cli = MongoClient()
journal = cli.critique.journal

res = journal.find({'info.type':'film'})

for film in res:
    imdb_id = film['info'][0]['imdb_id']
    if not imdb_id:
        continue
    subprocess.call(["scrapy runspider imdb_spider.py -t json --nolog -a search='%s' -o - > ttt.json" % imdb_id], shell=True)
    with codecs.open('ttt.json', 'a+', 'utf-8') as f:
        info = json.loads(f.readlines()[1])
        artists = []
        for a in info['artists']:
            artists.append({'artist': a})
        img_link = info['image_src']
        img_idx = img_link.rfind('/') + 1
        img_id = img_link[img_idx:]
        img_path = "/home/mtu/sc_crawler/images/films/" + img_id
        if not os.path.isfile(img_path):
            urllib.urlretrieve(img_link + ".UY600.jpg", "/home/mtu/sc_crawler/images/films/" + img_id)
        journal.find_one_and_update({'info.imdb_id': imdb_id},
                                    {'$set': {'info.$.titles': [{'vf': info['title_vf']}, {'vo': info['title_vo']}],
                                              'info.$.artists': info['artists'],
                                              'info.$.year': info['year'],
                                              'info.$.image': img_id}})
        i += 1
        print i, imdb_id, info['title_vf']
        time.sleep(random.random()*2)

