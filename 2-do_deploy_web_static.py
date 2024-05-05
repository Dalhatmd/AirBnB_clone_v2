#!/usr/bin/python3
""" Compresses and deploys web static"""
from fabric.api import *
from os import path


env.user = 'ubuntu'
env.hosts = ['100.25.19.204', '54.157.159.85']
env.key_filename = '~/.ssh/id_rsa'


def deploy(archive_path):
    """Deploys archive to multiple servers"""

    if not path.exists(archive_path):
        return False

    timestamp = archive_path[-18:-4]
    try:
        put(archive_path, '/tmp/')
# create directory
        run('sudo mkdir -P /data/web_static/releases/\
                web_static_%s.tgz/' % timestamp)
# uncompress
        run('sudo tar -xzf /tmp/web_static_%s.tgz -C /data/webstatic/releases\
                /web_static_%s' % timestamp % timestamp)
# delete tar file
        run('sudo rm /tmp/web_static_%s.tgz' % timestamp)

# move files into web_static
        run('sudo mv /data/web_static/releases/web_static_%s/web_static/*\
            /data_web_static/releases/web_static_%s/' % timestamp % timestamp)

        # delete web_statc dir
        run('sudo rm -rf /data/web_static/releases/web_static_%s/\
                web_static' % timestamp)

        # delete existing sym link
        run('sudo rm /tmp/web_static/current')

        # create new symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))

    except Exception as e:
        return False
    return True
