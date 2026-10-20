#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

# Replace these with your real web-01 and web-02 IPs when available
env.hosts = ['34.201.61.xx', '54.157.32.xx']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    Returns the archive path if the archive has been correctly generated.
    Otherwise, returns None
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)

        print("Packing web_static to {}".format(archive_path))
        result = local("tar -cvzf {} web_static".format(archive_path))

        if result.failed:
            return None

        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))

        return archive_path
    except Exception:
        return None


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


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
