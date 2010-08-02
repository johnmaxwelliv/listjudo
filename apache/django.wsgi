import site
site.addsitedir('/srv/li-dev/venv/lib/python2.6/site-packages')

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'my.settings'

sys.path.append('/home/johniv/Dropbox/li')
sys.path.append('/home/johniv/Dropbox/li/my')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
