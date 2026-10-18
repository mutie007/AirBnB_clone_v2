#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""
from fabric.api import local
from datetime import datetime
import os


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
