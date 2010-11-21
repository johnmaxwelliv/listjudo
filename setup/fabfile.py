from fabric.context_managers import settings
from fabric.contrib.files import contains
import fabric
import time
import unipath

_Path = unipath.Path

settings_file = _Path(__file__).parent.parent.child('settings.py')
django_settings = {'__file__': settings_file}
execfile(settings_file, django_settings)
g = globals()
for attribute in ['SITE_CODE', 'REPO_ROOT', 'SITE_ROOT']:
    g[attribute] = django_settings[attribute]

me = 'john'
setup = _Path(__file__).parent

repo_symlink = SITE_ROOT.child('repo')

local_host_string = 'root@localhost'
remote_host_string = 'root@173.230.145.81'

def _run(*args, **kwargs):
    return fabric.api.run(args[0] % args[1:], pty=True, **kwargs)

def isub(configure_apache=False):
    '''Initialize a site that's synced to a subdomain of jm9.us'''
    with settings(host_string=local_host_string):
        _init(SITE_CODE, REPO_ROOT, SITE_ROOT, remote=False, database='sqlite3')
    with settings(host_string=remote_host_string):
        _run("mkdir -p %s", SITE_ROOT)
        with settings(warn_only=True):
            _run("ln -s %s %s", REPO_ROOT, repo_symlink)
        if configure_apache:
            _init(SITE_CODE, repo_symlink, SITE_ROOT, remote=True, database='sqlite3', conf='synced.conf')
        else:
            _init(SITE_CODE, repo_symlink, SITE_ROOT, remote=True, database='sqlite3')

def prf():
    '''Refresh pypi dependencies everywhere and touch remote wsgi file'''
    with settings(host_string=local_host_string):
        _refresh(REPO_ROOT, SITE_ROOT, remote=False)
    with settings(host_string=remote_host_string):
        _refresh(repo_symlink, SITE_ROOT, remote=True)

def rf():
    '''Touch remote wsgi file'''
    with settings(host_string=remote_host_string):
        _run("touch %s", repo_symlink.child('setup').child('django.wsgi'))

def _init(site_code, repo_root, site_root, remote, database, conf=None):
    msgs = []
    _run("virtualenv --no-site-packages %s", site_root)
    _run("chmod +x %s", repo_root.child('manage.py'))
    _run("mkdir -p %s", site_root.child('media').child('public'))
    if database == 'sqlite3':
        _run("mkdir -p %s", site_root.child('db'))
        _run("touch %s", site_root.child('db').child('db.sqlite3'))
        _run("chmod -R a+w %s", site_root.child('db'))
    if remote:
        with settings(warn_only=True):
            _run("adduser --gecos=',,,' --disabled-login %s", site_code)
        # Make the site root writable so processes can put log files in it
        _run("chmod a+w %s %s", site_root)
        if conf:
            tmpconf = _Path('/tmp').child('tmp.httpd.%f.conf' % time.time())
            fabric.contrib.files.upload_template(setup.child(conf), tmpconf, context={
                'subdomain': site_code.replace('_', '-'),
                'site_code': site_code,
                'repo_root': repo_root,
                'site_root': site_root,
            })
            _run("cat %s >> /etc/apache2/httpd.conf", tmpconf)
            msgs.extend([
                '# edit apache configuration',
                'se /etc/apache2/httpd.conf',
                '# restart apache',
                'sudo /etc/init.d/apache2 graceful',
            ])
    _refresh(repo_root, site_root, remote=False)
    for msg in msgs:
        print(msg)

def _refresh(repo_root, site_root, remote):
    reqfile = repo_root.child('setup').child('pypi-requirements.txt')
    _run("pip install -E %s -r %s", site_root, reqfile)
    _run("pip freeze -E %s > %s", site_root, reqfile)
    _run("chown -R %s:%s %s", me, me, site_root)
    _run("chmod a+w %s", site_root.child('*.log'))
    if remote:
        _run("touch %s", repo_root.child('setup').child('django.wsgi'))
