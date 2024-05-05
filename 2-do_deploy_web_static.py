#!/usr/bin/python3
"""Compresses and deploys web static"""
from fabric.api import *
from os import path


env.user = 'ubuntu'
env.hosts = ['18.209.224.247', '100.26.252.22']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys archive to multiple servers"""

    if not path.exists(archive_path):
        return False

    timestamp = archive_path[-18:-4]
    try:
        put(archive_path, '/tmp/')

        run('sudo mkdir -p /data/web_static/releases/web_static_{}'
            .format(timestamp))

        run('sudo tar -xzf /tmp/web_static_{}.tgz -C\
            /data/web_static/releases/web_static_{}'
            .format(timestamp, timestamp))

        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        run('sudo mv /data/web_static/releases/web_static_{}/web_static/*               /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'\
                .format(timestamp))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/web_static_{} /data/web_static/current'.format(timestamp))

    except Exception as e:
        return False
    return True
