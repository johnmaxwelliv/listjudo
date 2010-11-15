import site
# enables importing unipath
site.addsitedir('/srv/py_base/lib/python2.6/site-packages')

from unipath import Path

settings_file = Path(__file__).parent.parent.child('settings.py')
this_file = __file__
__file__ = settings_file
execfile(settings_file)
__file__ = this_file

site.addsitedir(SITE_ROOT.child('lib').child('python2.6').child('site-packages'))

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

sys.path.append(REPO_ROOT)
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
