# Django localsettings for my project in development.

CACHE_BACKEND = 'locmem://'

INSTALL_ROOT = '/srv/li-dev/'

REPO_ROOT = '/home/john/Dropbox/li/'

FULLNAME = 'li-dev'

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': INSTALL_ROOT + 'db/db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
