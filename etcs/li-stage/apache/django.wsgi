import site
site.addsitedir('/srv/li-stage/lib/python2.6/site-packages')

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'my.settings'

sys.path.append('/srv/li-stage/li')
sys.path.append('/srv/li-stage/li/my')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
