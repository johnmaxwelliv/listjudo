from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *

import fabric
import os
import time
import random

MY_USERNAME = 'johniv'

# Refinement:
# Modularize for non-Dropbox staging schemes.
# Only use sudo when necessary?
# Make it so johniv owns the production application?
# Write a rollback function that switches to an older version of the app?

def run(*args, **kwargs):
    return fabric.api.run(*args, pty=True, **kwargs)

def sudo(*args, **kwargs):
    return fabric.api.run(*args, pty=True, **kwargs)

def h():
    print('linode_prep')
    print('system_setup as root')
    print('user_setup as ' + MY_USERNAME)
    print('apache_setup as root')
    print('deploy as root')

def linode_prep():
    messages = (
        "Did you choose Fremont for your Linode's datacenter?",
        "Did you deploy 32-bit Ubuntu 10.04 to your Linode?",
        "Did you record your Linode's root password?",
        "Did you boot up your Linode?",
        "Did you record your Linode's IP address ('eth0') in :c and :accounts?",
        "Did you log in to your Linode via the AJAX console, run 'ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub', and record the output in :c and :accounts?",
        "Did you attempt ssh in to your linode and make sure you were given the right RSA key fingerprint?",
        "Did you ssh in to localhost with your internet off and confirm the key fingerprint?",
    )
    for message in messages:
        if not confirm(message):
            quit()

def system_setup():
    sudo('aptitude update -y')
    sudo('aptitude full-upgrade -y')
    etckeeper_setup()
    hostname = raw_input('What do you want to name your new system? ')
    sudo('echo "%s" > /etc/hostname' % hostname)
    sudo('hostname -F /etc/hostname')
    ensure_single_sub('/etc/hosts', '^$', '%s\\t%s\\n' % ('127.0.0.1', hostname), use_sudo=True)
    etc('Configure hostname')
    if confirm("Would you like to ensure your new server's hostname is in your local /etc/hosts?"):
        ip = env.host
        if not confirm("Is %s is your Linode's IP address?" % ip):
            ip = raw_input("Please enter your Linode's IP address: ")
        with settings(host='localhost'):
            ensure_single_sub('/etc/hosts', '^$', '%s\\t%s\\n' % (ip, hostname), use_sudo=True)

    sudo('ln -sf /usr/share/zoneinfo/UTC /etc/localtime')
    etc('Set local time')

    packages = (
        'ack-grep',
        'less',
        'python-setuptools',
        'vim-nox', 
        'wget',
        'zsh',
    )
    sudo('aptitude -y install %s' % ' '.join(packages))
    etc('Install various packages with aptitude')

    sudo('easy_install pip')
    sudo('pip install ipython virtualenv')
    etc('Install various packages with pip')

    sudo('mkdir -p /srv/py-envs/')
    sudo('virtualenv --no-site-packages /srv/py-envs/base')

    with settings(warn_only=True):
        sudo('update-alternatives --set pager /bin/less')
        sudo('git config --system --bool color.ui true')
        sudo('git config --system --path core.pager less')
        sudo('git config --system diff.renames copy')
    etc('Change various preferences')

    sudo("adduser --shell=/usr/bin/zsh --gecos='John Maxwell,,,' --disabled-login " + MY_USERNAME)
    sudo("adduser johniv 'sudo'")
    etc('Add user ' + MY_USERNAME)
    print("Log in as root and run \npasswd " + MY_USERNAME + "\n to set " + MY_USERNAME + "'s password, then run user_setup with " + MY_USERNAME + " as the user")

def etckeeper_setup():
    if not exists('/etc/.git'):
        packages = (
            'bzr',
            'etckeeper',
            'git-core',
        )
        sudo('aptitude -y install %s' % ' '.join(packages))
        with settings(warn_only=True):
            sudo('etckeeper init')
        if not exists('/etc/.git'):
            sudo('etckeeper uninit -f')
            comment('/etc/etckeeper/etckeeper.conf', 'VCS="bzr"', use_sudo=True, char='# ', backup='.bak')
            uncomment('/etc/etckeeper/etckeeper.conf', 'VCS="git"', use_sudo=True, backup='.bak')
            sudo('rm /etc/etckeeper/etckeeper.conf.bak')
            sudo('etckeeper init')
        append('*.bak', '/etc/.gitignore', use_sudo=True)
        sudo('chmod -R a+rx /etc/.git')
        sudo('chmod a+w /etc/.git')
        sudo('chmod -R a+rx /etc/.etckeeper')
        sudo('aptitude -y remove bzr')
        etc('Initial commit')

def etc(message):
    with settings(warn_only=True):
        sudo('etckeeper commit "%s"' % message)

def ensure_single_sub(filename, before, after, use_sudo=False, **kwargs):
    search_pattern = after
    while search_pattern.endswith('\\n'):
        search_pattern = search_pattern[:len('\\n')]
    if not contains(search_pattern, filename, use_sudo):
        single_sub(filename, before, after, use_sudo, **kwargs)

def single_sub(filename, before, after, use_sudo=False, backup='.bak'):
    before = re.sub('/', '\\/', before)
    after = re.sub('/', '\\/', after)
    command = "sed -i%s -r -e '0,/%s/s//%s/' %s" % (backup, before, after, filename)
    if use_sudo:
        sudo(command, shell=False)
    else:
        run(command, shell=False)

def user_setup():
    with cd('~'):
        run('wget -O dropbox.tar.gz http://www.dropbox.com/download/?plat=lnx.x86')
        run('tar -zxof dropbox.tar.gz')
        run('rm dropbox.tar.gz')
        run('mkdir -p ~/tpe')
        run("wget -P ~/tpe 'http://www.dropbox.com/download?dl=packages/dropbox.py'")
        run('chmod +x ~/tpe/dropbox.py')
        run('touch ~/.cli-only')
        run('mkdir tb')
        run('mkdir .trashinfo')
        print('Visit the url in the output of the following command:')
        run('~/.dropbox-dist/dropboxd &')
        print("When you first log in, run")
        print("~/tpe/dropbox.py start")
        print("chmod +x ~/Dropbox/bin/*")
        print("~/Dropbox/bin/db-symlinks")
        print("Then log out.")

def files(name, sqlite=True):
    sudo('mkdir -p /srv/%s' % name)
    sudo('virtualenv --no-site-packages /srv/%s/venv' % name)
    for kind in ('request', 'error', 'application'):
        sudo('touch /srv/%s/%s.log' % (name, kind))
    sudo('chown -R %s:%s /srv/%s' % (MY_USERNAME, MY_USERNAME, name))
    sudo('chmod -R a+w /srv/%s/*.log' % name)
    if sqlite:
        sudo('mkdir -p /srv/%s/db' % name)
        sudo('touch /srv/%s/db/db.sqlite3' % name)
        sudo('chmod -R a+w /srv/%s/db' % name)

def apache_setup(project, devdir, devdomain, proddir, proddomain, error_email='xylowolf@gmail.com'):
    def setup(name, thisdir, thisdomain, sqlite=True, preinstall=True):
        files(name, i_own=i_own)
        if preinstall:
            sudo('pip install -E /srv/%s/venv -r %s/setup/requirements.txt' % (name, thisdir))
        sudo('chown -R %s:%s %s' % (MY_USERNAME, MY_USERNAME, thisdir))
        with settings(warn_only=True):
            sudo("adduser --shell=/usr/bin/zsh --gecos=',,,' --disabled-login %s" % name)
        with settings(warn_only=True):
            if confirm("Autogenerate httpd.conf?"):
                upload_template('%s/setup/httpd.conf' % devdir, '/tmp/%s.conf' % name, context = {
                    'domain': thisdomain,
                    'project_dir': thisdir,
                    'project': name,
                    'error_email': error_email,
                })
                sudo('chmod a+r /tmp/*.conf')
                sudo('cat /tmp/%s.conf >> /etc/apache2/httpd.conf' % name)
    try:
        prodname = project + '-prod'
        devname = project + '-dev'
        setup(prodname, proddir, proddomain, sqlite=True, preinstall=False)
        setup(devname, devdir, devdomain, sqlite=True, preinstall=True)
        with settings(warn_only=True):
            sudo('chmod a+w %s/db/.' % devdir)
            sudo('chmod a+w %s/db/*' % devdir)
        sudo('aptitude install -y apache2 apache2-dev libapache2-mod-wsgi')
        etc('Install apache and related packages')
        sudo('mkdir -p %s/my' % proddir)
        sudo('mkdir -p %s/apache' % proddir)

        sudo('a2enmod rewrite wsgi')
        etc('Enable apache module(s)')
    except:
        print("An error occurred!")
    finally:
        print("Fix apache configuration with\nsudo vim /etc/apache2/httpd.conf")
        print("Be sure to run\nsudo etckeeper commit\n after system configuration changes.")
        print("Fix production config with\nsudo vim %s/my/localsettings.py %s/apache/django.wsgi\n:n for next file" % (proddir, proddir))
        print("Fix database with\nsource /srv/%s/venv/bin/activate\n%s/my/\nmanage.py syncdb" % (prodname, proddir))
        print("and maybe\nsudo chmod a+w /srv/%s/db /srv/%s/db/*" % (prodname, prodname))
        print("Once that's all done, run \nsudo /etc/init.d/apache2 graceful")

def deploy(project, devdir, proddir):
    devname = project + '-dev'
    prodname = project + '-prod'
    ensure_relative_symlinks(devdir)
    if confirm("Do you have a clean working directory?"):
        sudo('cp -r %s %s/../%s' % (proddir, proddir, project + '-' + str(int(time.time()))))
        sudo('rsync -ahvEP %s/* %s --exclude-from=%s/setup/localfiles.txt' % (devdir, proddir, devdir))
        sudo('pip install -E /srv/%s/venv -r %s/setup/requirements.txt' % (prodname, proddir))
        with settings(warn_only=True):
            sudo('chmod -R a+w %s/db' % proddir)
        if confirm("Do you need to make changes to localsettings.py or django.wsgi or run migrations or syncdb?"):
            print("Stopping server...")
            sudo('apache2ctl -k graceful-stop')
            print("The production manage.py is at")
            print("%s/my" % proddir)
            print("Source syntax reminder:")
            print('source ../venv/bin/activate')
            print("Migration syntax reminder:")
            print("python manage.py migrate [appname]")
            print("When you've run all the migrations, execute")
            print("sudo /etc/init.d/apache2 start")
        else:
            sudo('touch %s/apache/django.wsgi' % proddir)

def ensure_relative_symlinks(directory):
    '''Will only work on local machine due to use of os module.'''
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames + dirnames:
            target = ''
            try:
                target = os.readlink(os.path.join(dirpath, filename))
            except OSError:
                pass
            if target:
                if target.startswith(os.path.sep):
                    raise AssertionError("%s points to %s (an absolute path)" % (filename, target))
