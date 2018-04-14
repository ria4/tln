import json, subprocess, sys
from datetime import date, timedelta

from django.http import HttpResponse


def get_boch(req, day=None):
    if day is None:
        d = date.today() - timedelta(6)
        day = d.strftime('%Y%m%d')

    subprocess.call(['/home/max/.virtualenvs/tln/bin/scrapy runspider /home/max/tln/boch/ent_spider.py -t json --nolog -a date=%s -o - > /home/max/tln/static/boch/boxoffice_ch.json' % day], shell=True)

    bo = {}
    with open('static/boch/boxoffice_ch.json', 'r') as f:
        lines = f.readlines()[1:-1]
        for line in lines:
            try:
                info = json.loads(line[:-2])
            except ValueError:
                info = json.loads(line[:-1])
            title = info['title']
            num = info['num']
            if title in bo:
                bo[title] += int(num)
            else:
                bo[title] = int(num)
    
    s = ''
    boo = [(k,bo[k]) for k in sorted(bo, key=bo.get, reverse=True)]
    print(boo)
    for i, (key, val) in enumerate(boo):
        s += '%s. %s (%s)<br/>' % (i+1, key, val)

    return HttpResponse(s)
