import logging
import os
import subprocess
import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.encoding import smart_str, filepath_to_uri
from django.utils.functional import curry

from photologue.models import Gallery, Photo, PhotoSizeCache

logger = logging.getLogger(__name__)

ET.register_namespace('', 'http://www.w3.org/2000/svg')

size_method_map_custom = {}


class GalleryCustom(models.Model):
    gallery = models.OneToOneField(Gallery, related_name='custom',
                                   on_delete=models.CASCADE)
    nav_title = models.CharField('Titre-menu du projet', max_length=63, blank=True)
    date_shooting = models.CharField('Date du projet', max_length=31)
    description_fr = models.TextField('Description FR', blank=True)
    description_en = models.TextField('Description EN', blank=True)
    allowed_users = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = u'Gallery Custom'
        verbose_name_plural = u'Galleries Custom'

    def __str__(self):
        return self.gallery.title


class PhotoCustom(models.Model):
    photo = models.OneToOneField(Photo, related_name='custom',
                                 on_delete=models.CASCADE)
    placeholder_width = models.IntegerField(default=0)
    placeholder_primitive_mode = models.IntegerField(default=1)
    placeholder_primitive_number = models.IntegerField(default=120)
    placeholder_blur = models.IntegerField(default=1)

    class Meta:
        verbose_name = u'Photo Custom'
        verbose_name_plural = u'Photos Custom'

    def _get_SIZE_size(self, size):
        # this should never be called for a non-placeholder size
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return Image.open(self.photo.image.storage.open(
            self._get_SIZE_filename(size))).size

    def _get_SIZE_url(self, size):
        # this should never be called for a non-placeholder size
        photosize = PhotoSizeCache().sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return '/'.join([
            self.photo.cache_url(),
            filepath_to_uri(self._get_filename_for_size(photosize.name))])

    def _get_SIZE_filename(self, size):
        # this should never be called for a non-placeholder size
        photosize = PhotoSizeCache().sizes.get(size)
        return smart_str(os.path.join(self.photo.cache_path(),
                                      self._get_filename_for_size(photosize.name)))

    def _get_filename_for_size(self, size):
        # this should never be called for a non-placeholder size
        size = getattr(size, 'name', size)
        base, ext = os.path.splitext(self.photo.image_filename())
        return ''.join([base, '_', size, '.svg'])

    def __getattr__(self, name):
        global size_method_map_custom
        if not size_method_map_custom:
            init_size_method_map_custom()
        di = size_method_map_custom.get(name, None)
        if di is not None:
            result = curry(getattr(self, di['base_name']), di['size'])
            setattr(self, name, result)
            return result
        else:
            return super().__getattr__(name)

    def size_exists(self, photosize):
        # this should never be called for a non-placeholder size
        func = getattr(self, "get_%s_filename" % photosize.name, None)
        if func is not None:
            if self.photo.image.storage.exists(func()):
                return True
        return False

    def create_size(self, photosize):
        if not photosize.name.endswith('_placeholder'):
            self.photo.create_size(photosize)
            return

        if self.size_exists(photosize):
            return

        namesplit = photosize.name.split('_')
        display_size, placeholder = '_'.join(namesplit[:-1]), namesplit[-1]

        photosize_display = PhotoSizeCache().sizes.get(display_size)
        if (photosize_display is None) or (placeholder != 'placeholder'):
            raise Exception('Invalid PhotoSize name!')

        if not self.photo.size_exists(photosize_display):
            self.photo.create_size(photosize_display)

        i_relpath = '/'.join([self.photo.cache_url(),
                             filepath_to_uri(self.photo._get_filename_for_size(display_size))])
        o_relpath = '/'.join([self.photo.cache_url(),
                             filepath_to_uri(self._get_filename_for_size(photosize.name))])
        i_path = os.path.abspath(i_relpath[1:])
        o_path = os.path.abspath(o_relpath[1:])
        cmd = '/usr/bin/npx sqip -i {} -o {} -w {} -m {} -n {} -b {}'.format( \
                    i_path,
                    o_path,
                    self.placeholder_width,
                    self.placeholder_primitive_mode,
                    self.placeholder_primitive_number,
                    self.placeholder_blur)
        try:
            subprocess.run(cmd.split(), timeout=180, check=True)
        except subprocess.CalledProcessError:
            logger.error('Creating a placeholder for %s returned a non-zero exit status!' % i_path)
        except subprocess.TimeoutExpired:
            logger.error('Creating a placeholder for %s timed out!' % i_path)

        try:
            tree = ET.parse(o_path)
            root = tree.getroot()
            dimensions = root.attrib['viewBox'].split()[2:4]
            root.attrib['width'] = dimensions[0] + 'px'
            root.attrib['height'] = dimensions[1] + 'px'
            tree.write(open(o_path, 'wb'))
        except Exception:
            logger.error('Writing placeholder dimensions for %s failed!' % i_path)

    def remove_size_placeholder(self, photosize, remove_dirs=True):
        if not self.size_exists(photosize):
            return
        filename = getattr(self, "get_%s_filename" % photosize.name)()
        if self.photo.image.storage.exists(filename):
            self.photo.image.storage.delete(filename)

    def clear_cache_placeholder(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            if photosize.name.endswith('_placeholder'):
                self.remove_size_placeholder(photosize, False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_ph_data = (self.placeholder_width,
                             self.placeholder_primitive_mode,
                             self.placeholder_primitive_number,
                             self.placeholder_blur)

    def save(self, *args, **kwargs):
        if self._old_ph_data != (self.placeholder_width,
                                 self.placeholder_primitive_mode,
                                 self.placeholder_primitive_number,
                                 self.placeholder_blur):
            self.clear_cache_placeholder()
            self._old_ph_data = (self.placeholder_width,
                                 self.placeholder_primitive_mode,
                                 self.placeholder_primitive_number,
                                 self.placeholder_blur)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.clear_cache_placeholder()
        self.photo.clear_cache()
        self.photo.image.storage.delete(self.photo.image.name)

    def __str__(self):
        return self.photo.title


@receiver(post_save, sender=Photo)
def create_photo_custom(sender, instance, created, **kwargs):
    if created:
        PhotoCustom.objects.create(photo=instance)

@receiver(post_save, sender=Photo)
def save_photo_custom(sender, instance, **kwargs):
    instance.custom.save()

@receiver(pre_delete, sender=Photo)
def clear_photo_custom(sender, instance, **kwargs):
    instance.custom.delete()


def init_size_method_map_custom():
    global size_method_map_custom
    for size in PhotoSizeCache().sizes.keys():
        if size.endswith('_placeholder'):
            size_method_map_custom['get_%s_size' % size] = \
                {'base_name': '_get_SIZE_size', 'size': size}
            size_method_map_custom['get_%s_url' % size] = \
                {'base_name': '_get_SIZE_url', 'size': size}
            size_method_map_custom['get_%s_filename' % size] = \
                {'base_name': '_get_SIZE_filename', 'size': size}
