#!/usr/bin/env bash
# Sets up the servers for depeloyment of web_static

sudo apt-get update

#install ngnix
sudo apt-get install -y nginx

#creates directories

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html

#test html page 
sudo echo "Server seems to be working" | sudo tee /data/web_static/releases/test/index.html

#removes symbolic link if exists
rm -f /data/web_static/current

#creates symbolic link
ln -s /data/web_static/releases/test/ /data/web_static/current

# Grants ownershio to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/


#serves content of current to hbnb_static

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart
