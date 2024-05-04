#!/usr/bin/python3
""" Creates a .tgz file """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """ creates a .tgz file """
    if not os.path.exists('versions'):
        os.makedirs('versions')

    now = datetime.now()
    archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
    archive_path = f"versions/{archive_name}"

    try:
        local(f"tar -czvf {archive_path} web_static")

        return archive_path
    except Exception as e:
        print(f"An error occurred while creating the archive: {e}")
        return None

