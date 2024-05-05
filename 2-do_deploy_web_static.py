#!/usr/bin/python3
""" Deploys to servers """
from fabric.api import *
import os


WEB_SERVERS = [
        {
            "host": "100.25.19.204",
            "user": "ubuntu",
            "key_filename": "~/.ssh/id_rsa",
            },
        {
            "host": "54.157.159.85",
            "user": "ubuntu",
            "key_filename": "~/.ssh/id_rsa",
            },
        ]


@task
def do_deploy(archive_path):
    """Deploys archive to multiple servers"""

    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    if not archive_filename.endswith(".tgz"):
        return False

    base_name = archive_filename[:-4]

    target_dir = f"/data/web_static/releases/{base_name}"

    successful = True
    for server in WEB_SERVERS:
        try:
            conn = Connection(
                host=server["host"],
                user=server["user"],
                connect_kwargs={
                    "key_filename": server["key_filename"],
                },
            )

            conn.put(archive_path, "/tmp/")

            conn.run(f"sudo mkdir -p {target_dir}")

            conn.run(f"sudo tar -xzf /tmp/{archive_filename} -C {target_dir}")

            conn.run(f"sudo rm /tmp/{archive_filename}")

            conn.run(f"sudo mv {target_dir}/web_static/_{timestamp}* {target_dir}_{timestamp}/")

            conn.run(f"sudo rm -rf {target_dir}/web_static/releases/web_static_{timestamp}/web_static")

            conn.run(f"sudo rm -rf /data/web_static/current")

            conn.run(f"sudo ln -s {target_dir}_{timestamp} /data/web_static/current")

        except Exception as e:
            successful = False

    return successful
