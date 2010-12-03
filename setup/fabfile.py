from fabric.context_managers import settings
from fabric.contrib.console import confirm
from fabric.contrib.files import contains
import fabric
import time
import unipath

_Path = unipath.Path

with open(_Path(__file__).parent.child('site.txt'), 'r') as f:
    SITE_CODE = f.read().rstrip('\n')

site_settings_file = _Path(__file__).parent.child(SITE_CODE).child('settings.py')
site_settings = {}
execfile(site_settings_file, site_settings)
g = globals()
for attribute in ['REPO_ROOT', 'SITE_ROOT', 'UPSTREAM_SITE']:
    g[attribute] = site_settings[attribute]

me = 'john'
setup = _Path(__file__).parent

repo_symlink = SITE_ROOT.child('repo')

local_host_string = 'root@localhost'
remote_host_string = 'root@173.230.145.81'

def _run(*args, **kwargs):
    return fabric.api.run(args[0] % args[1:], pty=True, **kwargs)

def confirm_site():
    if not confirm(SITE_CODE):
        exit()

def imain():
    confirm_site()
    '''Initialize a site that's downstream from another site'''
    with settings(host_string=remote_host_string):
        _run("mkdir -p %s", REPO_ROOT)
        # FIXME
        # We shouldn't be assuming the upstream site follows the srv site root convention
        _run('rsync -ahvEP --del %s %s', _Path('/srv').child(UPSTREAM_SITE).child('repo').child('*'), REPO_ROOT)
        _init(SITE_CODE, SITE_ROOT.child('repo'), SITE_ROOT, remote=True, database='sqlite3')

def push():
    with settings(host_string=remote_host_string):
        _run('rsync -ahvEP --del %s %s', _Path('/srv').child(UPSTREAM_SITE).child('repo').child('*'), REPO_ROOT)
        _refresh(REPO_ROOT, SITE_ROOT, True)

def isub(configure_apache=False):
    confirm_site()
    '''Initialize a site that's synced to a subdomain of jm9.us'''
    with settings(host_string=local_host_string):
        _init(SITE_CODE, REPO_ROOT, SITE_ROOT, remote=False, database='sqlite3')
    with settings(host_string=remote_host_string):
        _run("mkdir -p %s", SITE_ROOT)
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
    with settings(warn_only=True):
        _run("ln -s %s %s", repo_root, site_root.child('repo'))
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
        _run("chmod a+w %s", site_root)
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
    pip = site_root.child('bin').child('pip')
    _run("%s install -E %s -r %s", pip, site_root, reqfile)
    _run("%s freeze -E %s > %s", pip, site_root, reqfile)
    _run("chown -R %s:%s %s", me, me, site_root)
    _run("chmod a+w %s", site_root.child('*.log'))
    if remote:
        _run("touch %s", repo_root.child('setup').child('django.wsgi'))
