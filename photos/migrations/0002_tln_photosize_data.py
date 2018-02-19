# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def initial_photosizes(apps, schema_editor):

    PhotoSize.objects.create(name='tln_display',
                             width=1920,
                             height=1080,
                             crop=False,
                             upscale=False,
                             pre_cache=True,
                             increment_count=True)


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_photosizes),
    ]
