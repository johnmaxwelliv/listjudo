# Django localsettings for my project in staging.

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

INSTALL_ROOT = '/srv/li-stage/'

REPO_ROOT = '/srv/li-stage/li/'

FULLNAME = 'li-stage'

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': FULLNAME,                      # Or path to database file if using sqlite3.
        'USER': FULLNAME,                      # Not used with sqlite3.
        'PASSWORD': 'WQQIpSgvDczKpTjSDFaO',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
