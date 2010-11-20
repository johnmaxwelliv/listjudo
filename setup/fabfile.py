from fabric.context_managers import settings
from fabric.contrib.files import contains
from unipath import Path as _Path
import fabric
import time

me = 'john'
setup = _Path(__file__).parent

settings_file = _Path(__file__).parent.parent.child('settings.py')
this_file = __file__
__file__ = settings_file
execfile(settings_file)
__file__ = this_file
repo_symlink = SITE_ROOT.child('repo')

local_host_string = 'root@localhost'
remote_host_string = 'root@173.230.145.81'

def _run(*args, **kwargs):
    return fabric.api.run(args[0] % args[1:], pty=True, **kwargs)

def init_synced():
    with settings(host_string=local_host_string):
        _init(SITE_CODE, REPO_ROOT, SITE_ROOT, remote=False, database='sqlite3')
    with settings(host_string=remote_host_string):
        _run("mkdir -p %s", SITE_ROOT)
        with settings(warn_only=True):
            _run("ln -s %s %s", REPO_ROOT, repo_symlink)
        _init(SITE_CODE, repo_symlink, SITE_ROOT, remote=True, database='sqlite3', conf='synced.conf')

def rf():
    with settings(host_string=local_host_string):
        _refresh(REPO_ROOT, SITE_ROOT, remote=False)
    with settings(host_string=remote_host_string):
        _refresh(repo_symlink, SITE_ROOT, remote=True)

def _init(site_code, repo_root, site_root, remote, database, conf=None):
    _run("virtualenv --no-site-packages %s", site_root)
    _run("chmod +x %s", repo_root.child('manage.py'))
    if database == 'sqlite3':
        _run("mkdir -p %s", site_root.child('db'))
        _run("touch %s", site_root.child('db').child('db.sqlite3'))
        _run("chmod -R a+w %s", site_root.child('db'))
    if remote:
        with settings(warn_only=True):
            _run("adduser --gecos=',,,' --disabled-login %s", site_code)
        for kind in ('error', 'request'):
            _run("touch %s", site_root.child(kind + '.log'))
            _run("chmod a+w %s", site_root.child(kind + '.log'))
        tmpconf = _Path('/tmp').child('tmp.httpd.%f.conf' % time.time())
        fabric.contrib.files.upload_template(setup.child(conf), tmpconf, context={
            'subdomain': site_code.replace('_', '-'),
            'site_code': site_code,
            'repo_root': repo_root,
            'site_root': site_root,
        })
        #_run("cat %s >> /etc/apache2/httpd.conf", tmpconf)
        _refresh(repo_root, site_root, remote=True)
        print('# edit apache configuration')
        print('se /etc/apache2/httpd.conf')
        print('# restart apache')
        print('sudo /etc/init.d/apache2 graceful')
    else:
        _refresh(repo_root, site_root, remote=False)

def _refresh(repo_root, site_root, remote):
    reqfile = repo_root.child('setup').child('pypi-requirements.txt')
    statefile = _Path('/tmp').child('pypi-state.txt')
    diffs = _Path('/tmp').child('pypi-diffs.txt')
    _run("pip freeze -E %s > %s", site_root, statefile)
    _run("echo `diff %s %s` > %s", statefile, reqfile, diffs)
    if contains('<', diffs) or contains('>', diffs):
        _run("pip install -E %s -r %s", site_root, reqfile)
        _run("pip freeze -E %s > %s", site_root, reqfile)
        _run("chown -R %s:%s %s", me, me, site_root)
    _run("rm %s", statefile)
    _run("rm %s", diffs)
    if remote:
        _run("touch %s", repo_root.child('setup').child('django.wsgi'))
