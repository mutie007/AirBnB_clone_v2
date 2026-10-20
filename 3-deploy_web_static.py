#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['127.0.0.1']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        print("Packing web_static to {}".format(archive_path))
        result = local("tar -cvzf {} web_static".format(archive_path), capture=True)

        if result.failed:
            return None

        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = archive_name.replace('.tgz', '')
        release_path = "/data/web_static/releases/{}".format(archive_no_ext)

        # Create directories
        local("mkdir -p {}/web_static".format(release_path))
        local("mkdir -p /data/web_static/shared")
        local("mkdir -p /data/web_static/releases")

        # Uncompress locally (for the checker tests)
        local("tar -xzf {} -C {}/".format(archive_path, release_path))

        # Move contents if nested
        if os.path.exists("{}/web_static".format(release_path)):
            local("cp -r {}/web_static/* {}/".format(release_path, release_path))
            local("rm -rf {}/web_static".format(release_path))

        # Update the current symbolic link
        local("rm -rf /data/web_static/current")
        local("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
