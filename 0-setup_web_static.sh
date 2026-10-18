#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create / recreate the symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"

# Add the location block if it doesn't already exist
if ! grep -q "hbnb_static" "$config_file"; then
    sed -i '/listen 80 default_server;/a\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"
fi

# Restart Nginx
service nginx restart

exit 0
