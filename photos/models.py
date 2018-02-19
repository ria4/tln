from PIL import Image

from django.db import models
from django.utils.functional import curry

from photologue.models import Gallery, Photo, PhotoSize

max_size_method_map = {}


class PhotoMaxSize(PhotoSize):
    max_width = models.PositiveIntegerField('max width', default=0)
    max_height = models.PositiveIntegerField('max height', default=0)


class PhotoMaxSizeCache(object):
    __state = {"max_sizes": {}}

    def __init__(self):
        self.__dict__ = self.__state
        if not len(self.max_sizes):
            max_sizes = PhotoMaxSize.objects.all()
            for max_size in max_sizes:
                self.max_sizes[max_size.name] = max_size

    def reset(self):
        global max_size_method_map
        max_size_method_map = {}
        self.max_sizes = {}


def init_max_size_method_map():
    global max_size_method_map
    for max_size in PhotoMaxSizeCache().max_sizes.keys():
        max_size_method_map['get_%s_max_size' % max_size] = \
            {'base_name': '_get_MAX_SIZE_max_size', 'max_size': max_size}
        max_size_method_map['get_%s_photomax_size' % max_size] = \
            {'base_name': '_get_MAX_SIZE_photomax_size', 'max_size': max_size}
        max_size_method_map['get_%s_url' % max_size] = \
            {'base_name': '_get_MAX_SIZE_url', 'max_size': max_size}
        max_size_method_map['get_%s_filename' % max_size] = \
            {'base_name': '_get_MAX_SIZE_filename', 'max_size': max_size}


class PhotoCustom(Photo):

    def _get_MAX_SIZE_photosize(self, size):
        return PhotoMaxSizeCache().max_sizes.get(size)

    def _get_MAX_SIZE_size(self, size):
        photosize = PhotoMaxSizeCache().max_sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        return Image.open(self.image.storage.open(
            self._get_MAX_SIZE_filename(size))).size

    def _get_MAX_SIZE_url(self, size):
        photosize = PhotoMaxSizeCache().max_sizes.get(size)
        if not self.size_exists(photosize):
            self.create_size(photosize)
        if photosize.increment_count:
            self.increment_count()
        return '/'.join([
            self.cache_url(),
            filepath_to_uri(self._get_filename_for_size(photosize.name))])

    def _get_MAX_SIZE_filename(self, size):
        photosize = PhotoMaxSizeCache().max_sizes.get(size)
        return smart_str(os.path.join(self.cache_path(),
                                      self._get_filename_for_size(photosize.name)))

    def __getattr__(self, name):
        global max_size_method_map
        if not max_size_method_map:
            init_max_size_method_map()
        di = max_size_method_map.get(name, None)
        if di is not None:
            result = curry(getattr(self, di['base_name']), di['max_size'])
            setattr(self, name, result)
            return result
        else:
            return super().__getattr__(name)

    def resize_image(self, im, photosize):
        """
        We ignore the width and height attributes which could have been passed
        to a PhotoMaxSize model (this is a PhotoSize job).
        Also, there is no cropping. (But note that the image lay be upscaled.)
        """
        if not isinstance(photosize, PhotoMaxSize):
            return super().resize_image(im, photosize)

        cur_width, cur_height = im.size
        max_width, max_height = photosize.max_width, photosize.max_height
        if not max_width == 0 and not max_height == 0:
            ratio = min(float(max_width) / cur_width,
                        float(max_height) / cur_height)
        else:
            # Setting only one of max_width or max_height is basically
            # setting a width/height: use the Photo model...
            return im
        new_dimensions = (int(round(cur_width * ratio)),
                          int(round(cur_height * ratio)))
        if new_dimensions[0] > cur_width or \
           new_dimensions[1] > cur_height:
            if not photosize.upscale:
                return im
        return im.resize(new_dimensions, Image.ANTIALIAS)



class GalleryCustom(models.Model):
    gallery = models.OneToOneField(Gallery, related_name='custom',
                                   on_delete=models.CASCADE)
    date_shooting = models.CharField('Date du projet', max_length=31)
    description_fr = models.TextField('Description FR', blank=True)
    description_en = models.TextField('Description EN', blank=True)

    class Meta:
        verbose_name = u'Gallery Custom'
        verbose_name_plural = u'Galleries Custom'

    def __str__(self):
        return self.gallery.title
