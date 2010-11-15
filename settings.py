import site

from unipath import Path

REPO_ROOT = Path(__file__).parent
with open(REPO_ROOT.child('setup').child('site.txt'), 'r') as f:
    SITE_CODE = f.read().rstrip('\n')
SITE_ROOT = Path('/srv').child(SITE_CODE)

site.addsitedir(REPO_ROOT)
site.addsitedir(REPO_ROOT.child('my'))
site.addsitedir(REPO_ROOT.child('lib'))

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@campuseagle.com'
EMAIL_HOST_PASSWORD = 'flamezoo491'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '! '

ADMINS = (
    ('John Maxwell', 'jmiv.error@gmail.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = SITE_ROOT.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

DJANGO_STATIC = False
DJANGO_STATIC_MEDIA_URL = '/media'
DJANGO_STATIC_SAVE_PREFIX = MEDIA_ROOT.child('public').child('build')
DJANGO_STATIC_NAME_PREFIX = '/public/build'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/public/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*n+f1*pji*)2qh@%&1k))&7mp14qx&*l&$onr$&_za!)(mx6-b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/john/li/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'debug_toolbar',
    'south',
    'djangoratings',
    'lists',
    'uni-form',
    'ajax_validation',
    'oembed',
    'imagekit',
    'django_static',
    'django.contrib.webdesign',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

INTERNAL_IPS = ('127.0.0.1', '24.130.12.146', '24.130.13.211')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
}

CONSUMER_URLIZE_ALL = False

site_settings = REPO_ROOT.child('setup').child(SITE_CODE).child('settings.py')
execfile(site_settings)
