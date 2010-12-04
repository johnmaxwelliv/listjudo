from unipath import Path

SITE_ID = 2
_SITE_CODE = 'li_prod'
UPSTREAM_SITE = 'li_dev'
SITE_ROOT = Path('/srv').child(_SITE_CODE)
REPO_ROOT = SITE_ROOT.child('repo')

DEBUG = False
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

MEDIA_URL = '/media/repo'
