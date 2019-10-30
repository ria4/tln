#!/usr/bin/python
# coding: utf-8

import binascii, codecs, json, os, random, subprocess, time, urllib, shutil, requests

from PIL import Image
from pymongo import MongoClient


def download_distant_image(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        h = binascii.hexlify(os.urandom(16))
        local_url = h.decode('ascii')
        with open('critique/static/critique/tmp/%s' % local_url, 'wb') as f:
           shutil.copyfileobj(r.raw, f)
        baseheight = 300
        img = Image.open('critique/static/critique/tmp/%s' % local_url)
        hpercent = baseheight/float(img.size[1])
        wsize = int(float(img.size[0])*float(hpercent))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save('critique/static/critique/%s.jpg' % local_url)
        os.remove('critique/static/critique/tmp/%s' % local_url)
        return 'critique/%s.jpg' % local_url
    return ''


cli = MongoClient()
journal = cli.critique_django.oeuvre

res = journal.find({'info.type':'serie'})

i = 0
for film in res:
    if not 'imdb_id' in film['info'] or not film['info']['imdb_id']:
        print 'XXX', film['info']['titles']['vf']
        continue
    imdb_id = film['info']['imdb_id']
    subprocess.call(["scrapy runspider imdb_spider.py -t json --nolog -a search='%s' -o - > ttt.json" % imdb_id], shell=True)
    with codecs.open('ttt.json', 'a+', 'utf-8') as f:
        info = json.loads(f.readlines()[1])
        img_link = info['image_src']
        img_url = download_distant_image(img_link + ".UY300.jpg")
        journal.find_one_and_update({'info.imdb_id': imdb_id},
                                    {'$set': {'info.image_url': img_url}})
        i += 1
        print i, imdb_id, info['title_vf']
        time.sleep(random.random()*2)

