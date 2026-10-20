#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
import os

# Replace these with your real web-01 and web-02 IPs when available
env.hosts = ['34.201.61.xx', '54.157.32.xx']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    Returns True if all operations have been done correctly,
    otherwise returns False
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_ext = archive_name.replace('.tgz', '')
        release_path = "/data/web_static/releases/{}/".format(archive_no_ext)

        # Upload archive to /tmp/
        put(archive_path, "/tmp/")

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))

        # Delete the archive from the server
        run("rm /tmp/{}".format(archive_name))

        # Move contents out of the nested web_static folder
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static folder
        run("rm -rf {}web_static".format(release_path))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False
