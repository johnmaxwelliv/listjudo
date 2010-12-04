from unipath import Path
import os

me = 'john'

_SITE_CODE = 'li_dev'
UPSTREAM_SITE = None
SITE_ROOT = Path('/srv').child(_SITE_CODE)
REPO_ROOT = Path('/home').child('john').child('li')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': SITE_ROOT.child('db').child('db.sqlite3'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'dummy://'

if os.path.exists('/home/john/.cli-only'):
    MEDIA_URL = '/media/repo'
else:
    MEDIA_URL = 'http://127.0.0.1:8888/media/repo'
