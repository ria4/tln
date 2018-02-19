# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations

from photos.models import PhotoMaxSize


def initial_photosizes(apps, schema_editor):

    # If there are already PhotoMaxSizes, then we are upgrading an existing
    # installation, we don't want to auto-create some PhotoMaxSizes.
    if PhotoMaxSize.objects.all().count() > 0:
        return
    PhotoSizeCustom.objects.create(name='max_display',
                                   max_width=1920,
                                   max_height=1080,
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
