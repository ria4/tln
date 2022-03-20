"""
Django settings for tln project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_comments',
    'zinnia',
    'photologue',
    'sortedm2m',
    'tagging',
    'mptt',
    'home',
    'blog',
    'photos',
    'critique',
    'tln',
]

COMMENTS_APP = 'django_comments'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tln.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tln/templates/tln'),
                 os.path.join(BASE_DIR, 'home/templates'),
                 os.path.join(BASE_DIR, 'blog/templates'),
                 os.path.join(BASE_DIR, 'photos/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': '<<invalid variable>>',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.entry_default',
                'critique.context_processors.oeuvre_form',
                'critique.context_processors.comment_form',
                'critique.context_processors.seance_form',
                'photos.context_processors.gallery_list',
                'tln.context_processors.login_form',
                'tln.context_processors.android',
                'tln.context_processors.webkit',
                'zinnia.context_processors.version',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = ['django.core.context_processors.request']

WSGI_APPLICATION = 'tln.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = "/#login"


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Models

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Haystack configuration

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        #'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
#    },
#}

SITE_ID = 1


# Zinnia configuration

#ZINNIA_ENTRY_BASE_MODEL = 'blog.models.EntryCustom'
ZINNIA_PREVIEW_MAX_WORDS = 100
ZINNIA_PAGINATION = None
ZINNIA_PROTOCOL = 'https'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{levelname}] ({asctime}) {message}',
            'style': '{',
            },
        },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': '/home/ria/tln/net/django_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
