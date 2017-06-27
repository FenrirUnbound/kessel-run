#!/bin/sh

set -eu

#####
# Make app engine libraries accessible
#####
apt-get update
apt-get install unzip -y
curl -s -o google_appengine.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.56.zip
unzip -q google_appengine.zip
rm google_appengine.zip
