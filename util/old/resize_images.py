
import os
import sys
from PIL import Image

baseheight = 300
img = Image.open(sys.argv[1])
hpercent = baseheight/float(img.size[1])
wsize = int(float(img.size[0])*float(hpercent))
img = img.resize((wsize, baseheight), Image.ANTIALIAS)
img.save('%s.jpg' % sys.argv[1])
os.remove(sys.argv[1])

