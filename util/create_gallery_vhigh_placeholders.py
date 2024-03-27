#!/usr/bin/python

"""
# vtln
(tln)$ python create_gallery_vhigh_placeholders.py 'gallery-slug'

Creates missing PhotoCustom instances and corresponding vhigh_display placeholders.
Run it from the main tln folder when opening a new gallery.
"""

import django
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.path.append('/home/ria/tln')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tln.settings')
django.setup()

from django.utils.encoding import filepath_to_uri

from photologue.models import Gallery, Photo, PhotoSizeCache
from photos.models import PhotoCustom

ET.register_namespace('', 'http://www.w3.org/2000/svg')


def create_missing_photocustoms(gallery_slug):
    gallery = Gallery.objects.get(slug=gallery_slug)
    for p in gallery.photos.all().order_by('id'):
        obj, created = PhotoCustom.objects.get_or_create(photo=p)
        if created:
            print('Created PhotoCustom instance for Photo "%s"' % p.title)
        else:
            print('PhotoCustom instance already present for Photo "%s"' % p.title)
    print()


def create_missing_vhigh_placeholders(gallery_slug):

    gallery = Gallery.objects.get(slug=gallery_slug)

    photocustoms = []
    for p in gallery.photos.all().order_by('id'):
        photocustoms.append(PhotoCustom.objects.get(photo_id=p.id))
    n = len(photocustoms)

    print('Found %d photos in gallery "%s"\n' % (n, gallery.title))


    for i, pc in enumerate(photocustoms):

        photosize = PhotoSizeCache().sizes.get('vhigh_display_placeholder')
        if pc.size_exists(photosize):
            print('Placeholder already exists for "%s" at %s' % (pc.photo.title, pc._get_SIZE_url('vhigh_display_placeholder')))
            continue

        display_size = 'vhigh_display'
        photosize_display = PhotoSizeCache().sizes.get(display_size)

        if not pc.photo.size_exists(photosize_display):
            pc.photo.create_size(photosize_display)
            print('Created %s' % pc.photo._get_filename_for_size(display_size))

        i_relpath = '/'.join([pc.photo.cache_url(),
                             filepath_to_uri(pc.photo._get_filename_for_size(display_size))])
        o_relpath = '/'.join([pc.photo.cache_url(),
                             filepath_to_uri(pc._get_filename_for_size(photosize.name))])
        i_path = os.path.abspath(i_relpath[1:])
        o_path = os.path.abspath(o_relpath[1:])
        cmd = '/usr/bin/npx sqip -o {} -m {} -n {} -b {} {}'.format( \
                    o_path,
                    self.placeholder_primitive_mode,
                    self.placeholder_primitive_number,
                    self.placeholder_blur,
                    i_path)
        #cmd = '/usr/bin/npx sqip -i {} -o {} -w {} -m {} -n {} -b {}'.format( \
        #            i_path,
        #            o_path,
        #            pc.placeholder_width,
        #            pc.placeholder_primitive_mode,
        #            pc.placeholder_primitive_number,
        #            pc.placeholder_blur)
        try:
            subprocess.run(cmd.split(), timeout=180, check=True)
            print('Created a placeholder for photo "%s" (%d / %d)' % (pc.photo.title, i+1, n))
        except subprocess.CalledProcessError:
            print('Creating a placeholder for %s returned a non-zero exit status!' % i_path)
            sys.exit()
        except subprocess.TimeoutExpired:
            print('Creating a placeholder for %s timed out!' % i_path)
            sys.exit()

        try:
            tree = ET.parse(o_path)
            root = tree.getroot()
            dimensions = root.attrib['viewBox'].split()[2:4]
            root.attrib['width'] = dimensions[0] + 'px'
            root.attrib['height'] = dimensions[1] + 'px'
            tree.write(open(o_path, 'wb'))
            print('Updated placeholder SVG dimensions')
        except Exception:
            print('Writing placeholder dimensions for %s failed!' % i_path)
        print()


create_missing_photocustoms(sys.argv[1])
create_missing_vhigh_placeholders(sys.argv[1])
