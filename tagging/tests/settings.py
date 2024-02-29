"""Tests settings"""
import os

SECRET_KEY = 'secret-key'

DATABASES = {
    'default': {
        'NAME': 'tagging.db',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE')
if DATABASE_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tagging',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'postgres'
        }
    }
elif DATABASE_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tagging',
            'USER': 'root',
            'PASSWORD': 'mysql',
            'HOST': 'mysql',
            'TEST': {
                'COLLATION': 'utf8_general_ci'
            }
        }
    }

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'tagging',
    'tagging.tests',
]
